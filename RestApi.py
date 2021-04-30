import flask
from flask import request, abort, jsonify
import mysql.connector
import time
import requests
import json
import pymongo
import datetime
from time import gmtime, strftime

from flask import request
from pymongo.results import InsertOneResult

app = flask.Flask(__name__)
app.config["DEBUG"] = True
myclient = pymongo.MongoClient("mongodb+srv://Mist:1234@cluster0.uuxni.mongodb.net/AP2_EX2?retryWrites=true&w=majority")
mydb = myclient["AP2_EX2"]


@app.route("/api/model", methods=['POST'])
def train():
    modelType = request.args.get('model_type')
    if modelType != 'hybrid' and modelType != 'regression':
        abort(400)
    collist = mydb.list_collection_names()
    if "models" not in collist:
        isFirstTime = True
    else:
        models = mydb["models"]
        all_models = models.find()
        if all_models.count() == 0:
            isFirstTime = True
        else:
            isFirstTime = False
    datas = mydb["datas"]

    output_date = datetime.datetime.now().strftime(
        "%Y-%m-%dT%H:%M:%S+03.00")  # TODO: change +03.00 to our really time zone
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
        'model_id': bytes(str(x.inserted_id), 'utf-8'),
        'upload_time': bytes(output_date, 'utf-8'),
        'status': 'pending'
    }

    x = models.insert_one(new_model)

    return jsonify(response_model), 200


@app.route("/api/model", methods=['GET'])
def get_model():
    id = request.args.get('model_id')
    if id == None:
        abort(400)
    models = mydb["models"]
    query = {"_id": int(id)}

    wanted_model = models.find(query)
    if (wanted_model.count() != 1):
        abort(400)
    model = {
        'model_id': bytes(str(wanted_model[0]["_id"]), 'utf-8'),
        'upload_time': bytes(str(wanted_model[0]["upload_time"]), 'utf-8'),
        'status': bytes(str(wanted_model[0]["status"]), 'utf-8')
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
        abort(400)
    datas.delete_one(query)

    return ""


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9872)