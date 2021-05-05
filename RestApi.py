import flask
from flask import request, abort, jsonify
import time
import pymongo
import datetime
from datetime import datetime, timezone
from flask import request
from werkzeug.utils import redirect
import multiprocessing as mp
from flask import render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True
myclient = pymongo.MongoClient("mongodb+srv://Mist:1234@cluster0.uuxni.mongodb.net/AP2_EX2?retryWrites=true&w=majority")
mydb = myclient["AP2_EX2"]


def trainModel(idNumber):
    print("trained model num {idNumber}")
    time.sleep(5)
    datas = mydb["datas"]
    models=mydb["models"]
    query = {"_id": int(idNumber)}
    model=models.find(query)
    model[0]["status"]="ready"
    datas.delete_one(query)



def get_json_model_from_database(model):
    return  {
        'model_id': str(model["_id"]),
        'upload_time': str(model["upload_time"]),
        'status': str(model["status"])
    }

# @app.route('/')
# def home_page():
#     modelsDB = mydb["models"]
#     models_list = modelsDB.find().sort("_id", -1)
#     return render_template('index.html', models=models_list)

@app.route("/api/model", methods=['POST'])
def train():
    modelType = request.args.get('model_type')
    if modelType != 'hybrid' and modelType != 'regression':
        abort(400)
    collist = mydb.list_collection_names()
    models = mydb["models"]

    if "models" not in collist:
        isFirstTime = True
    else:
        if models.count_documents({}) == 0:
            isFirstTime = True
        else:
            isFirstTime = False
    datas = mydb["datas"]

    now = datetime.now()
    utc = now.replace(tzinfo=timezone.utc) - now.astimezone(timezone.utc)
    SECONDS_IN_HOUR = 3600

    output_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+" + str(utc.seconds/SECONDS_IN_HOUR))
    if isFirstTime:
        request.json["_id"] = 1
    else:
        max = models.find().sort("_id", -1).limit(1)
        request.json["_id"] = max[0]["_id"] + 1

    x = datas.insert_one(request.json)

    new_model = {
        "_id": x.inserted_id,
        "upload_time": output_date,
        "status": "pending",
        "type": modelType
    }
    response_model = {
        'model_id': str(x.inserted_id),
        'upload_time': output_date,
        'status': 'pending'
    }

    x = models.insert_one(new_model)
    #TODO: remeber, after you finish the learning process, delete the data document with that id from the "datas" db
    threadPool.apply_async(trainModel,(request.json["_id"]))
    return jsonify(response_model), 200


@app.route("/api/model", methods=['GET'])
def get_model():
    id = request.args.get('model_id')
    if id == None:
        abort(400)
    models = mydb["models"]
    query = {"_id": int(id)}

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
    query = {"_id": int(id)}

    wanted_model = models.delete_one(query)
    if (wanted_model.deleted_count != 1):
        abort(404)
    datas.delete_one(query)

    return ('', 204)


@app.route("/api/models", methods=["GET"])
def get_models():
    models = mydb["models"]
    all_models = models.find()
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
    query = {"_id": int(id)}

    wanted_model = models.find(query)
    if (models.count_documents(query) != 1):
        abort(404)
    if (wanted_model[0]['status'] == "pending"):
        return redirect("/api/model?model_id=" + str(id), 405)#TODO: decide if it does get and not post as writen in the document

    anomaly_datas = mydb["anomaly_datas"]#TODO: predict the anomalies, and delete from the database unnecessary docu,ents at the end
    request.json["_id"] = int(id) + 1
    x = anomaly_datas.insert_one(request.json)

    return ""


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9880)

threadPool = mp.Pool(20)
