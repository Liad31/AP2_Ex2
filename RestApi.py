import flask
from flask import  abort, jsonify
import pymongo
from pymongo.collation import Collation
import datetime
from datetime import datetime, timezone
from flask import request
from werkzeug.utils import redirect
import multiprocessing as mp
from flask import render_template
from AnomalyDetector import LinearAnomalyDetector,CircleAnomalyDetector
import pickle
import matplotlib.pyplot as plt
import mpld3
from graphCreator import plotGraph

app = flask.Flask(__name__)
app.config["DEBUG"] = True
myclient = pymongo.MongoClient("mongodb+srv://Mist:1234@cluster0.uuxni.mongodb.net/AP2_EX2?retryWrites=true&w=majority")
mydb = myclient["AP2_EX2"]

def trainModel(idNumber):
    myclient = pymongo.MongoClient(
        "mongodb+srv://Mist:1234@cluster0.uuxni.mongodb.net/AP2_EX2?retryWrites=true&w=majority")
    mydb = myclient["AP2_EX2"]
    datas = mydb["datas"]
    models=mydb["models"]
    query = {"_id": (idNumber)}
    model=models.find(query).limit(1)[0]
    data_query = {"_id": model["data_id"]}
    json=datas.find(data_query).next()["train_data"]
    if model["type"]=="regression":
        newModel=LinearAnomalyDetector(json)
    elif model["type"]=="hybrid":
        newModel=CircleAnomalyDetector(json)
    models.update_one(
    {"_id": idNumber}, {"$set":
        {"status":"ready","pickle":pickle.dumps(newModel,protocol=pickle.HIGHEST_PROTOCOL) } # new value will be 42
    })
    datas.delete_one(data_query)
def getAnomalies(modelId,dataId):
    myclient = pymongo.MongoClient(
        "mongodb+srv://Mist:1234@cluster0.uuxni.mongodb.net/AP2_EX2?retryWrites=true&w=majority")
    mydb = myclient["AP2_EX2"]
    models=mydb["models"]
    samples=mydb["anomaly_datas"]
    modelQuery={"_id": modelId}
    dataQuery={"_id": dataId}
    try:
        modelJson = models.find(modelQuery).next()
        model = pickle.loads(modelJson["pickle"])
        json = samples.find(dataQuery).next()["predict_data"]
        res=model.getAnomalySpan(json)
        correlated=[[i.strip() for i in str(x).split(',')] for x in model.getCorrelatedFeatures()]
        return {"anomalies":res,"reason":{"correlated_features":correlated,"algorithm":modelJson["type"]}}
    except Exception as e:
        print(e)
        return "detection error"
    finally:
        samples.delete_one(dataQuery)

if __name__=="__main__":
    models = mydb["models"]
    threadPool = mp.Pool(20)

def get_json_model_from_database(model):
    return  {
        'model_id': str(model["_id"]),
        'upload_time': str(model["upload_time"]),
        'status': str(model["status"])
    }

@app.route('/')
def home_page():
    modelsDB = mydb["models"]
    models_list = modelsDB.find().sort("_id", -1)
    return render_template('index.html', models=models_list)

@app.route("/api/model", methods=['POST'])
def train():
    modelType = request.args.get('model_type')
    if modelType != 'hybrid' and modelType != 'regression':
        abort(400)
    seqs = mydb["seqs"]
    models = mydb["models"]
    datas = mydb["datas"]

    now = datetime.now()
    utc = now.replace(tzinfo=timezone.utc) - now.astimezone(timezone.utc)
    SECONDS_IN_HOUR = 3600

    output_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+" + str(utc.seconds/SECONDS_IN_HOUR))
    request.json['_id'] = str(seqs.find_and_modify(
        query={ 'collection' : 'datas' },
        update={'$inc': {'id': 1}},
        fields={'id': 1, '_id': 0},
        new=True
    ).get('id'))
    x = datas.insert_one(request.json)

    new_model = {"upload_time": output_date, "status": "pending", "type": modelType, "pickle": "",
         "_id": str(seqs.find_and_modify(
             query={'collection': 'models'},
             update={'$inc': {'id': 1}},
             fields={'id': 1, '_id': 0},
             new=True
         ).get('id')),
        "data_id": x.inserted_id
    }
    x = models.insert_one(new_model)
    response_model = {
        'model_id': str(x.inserted_id),
        'upload_time': output_date,
        'status': 'pending'
    }
    threadPool.map_async(trainModel,(x.inserted_id,))
    return jsonify(response_model), 200


@app.route("/api/model", methods=['GET'])
def get_model():
    id = request.args.get('model_id')
    if id == None:
        abort(400)
    models = mydb["models"]
    query = {"_id": id}

    wanted_model = models.find(query)
    if (models.count_documents(query) != 1):
        abort(404)
    model = {
        'model_id': str(wanted_model[0]["_id"]),
        'upload_time': str(wanted_model[0]["upload_time"]),
        'status': str(wanted_model[0]["status"])
    }

    return jsonify(model), 200


@app.route("/api/model", methods=["DELETE"])
def delete_model():
    id = request.args.get('model_id')
    if id == None:
        abort(400)
    models = mydb["models"]
    datas = mydb["datas"]
    query = {"_id": id}
    wanted_model = models.find(query)[0]
    data_id = wanted_model["data_id"]
    query_data = {"_id": data_id}

    wanted_model = models.delete_one(query)
    if (wanted_model.deleted_count != 1):
        abort(404)
    datas.delete_one(query_data)

    return ('', 204)


@app.route("/api/models", methods=["GET"])
def get_models():
    models = mydb["models"]
    all_models = models.find().sort("_id", -1).collation(Collation(locale='en_US', numericOrdering=True))
    models_array = []
    for model in all_models:
        json_model = get_json_model_from_database(model)
        models_array.append(json_model)
    return jsonify(models_array), 200


@app.route("/api/anomaly", methods=["POST"])
def get_anomalies():
    id = request.args.get('model_id')
    if id == None:
        abort(400)
    models = mydb["models"]
    query = {"_id": id}

    wanted_model = models.find(query)
    if (models.count_documents(query) != 1):
        abort(404)
    if (wanted_model[0]["status"] == "pending"):
        return redirect("/api/model?model_id=" + str(id), 405)#TODO: decide if it does get and not post as writen in the document

    anomaly_datas = mydb["anomaly_datas"]
    seqs = mydb["seqs"]
    request.json['_id'] = str(seqs.find_and_modify(
        query={ 'collection' : 'anomaly_datas' },
        update={'$inc': {'id': 1}},
        fields={'id': 1, '_id': 0},
        new=True
    ).get('id'))
    x = anomaly_datas.insert_one(request.json)
    dataId=x.inserted_id
    res=threadPool.starmap(getAnomalies,[(id,dataId)])
    return jsonify(res)

@app.route("/api/graph", methods=["POST"])
def postGraph():
    ys = request.json["ys"]
    spans = request.json["spans"]
    plotGraph(ys, spans)
    return '', 200

@app.route("/api/get_graph", methods=["GET"])
def getGraph():
    return render_template('graph.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9876)
