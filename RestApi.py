import flask
from flask import request,abort
import mysql.connector
import time
import requests
import json
import pymongo

from flask import  request
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#REMOVE GET
@app.route("/api/model", methods=['POST','GET'])
def train():
    modelType= request.args.get('model_type')
    if modelType=='hybrid':
        pass
    elif modelType=='regression':
        pass
    else:
        abort(400)
    print(request.headers)
    print(request.json)


    return "hi"





























if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["AP2_EX2"]
    mycol = mydb["customers"]
    mydict = {"name": "John", "address": "Highway 37"}

    x = mycol.insert_one(mydict)
    mylist = [
        {"name": "Amy", "address": "Apple st 652"},
        {"name": "Hannah", "address": "Mountain 21"},
        {"name": "Michael", "address": "Valley 345"},
        {"name": "Sandy", "address": "Ocean blvd 2"},
        {"name": "Betty", "address": "Green Grass 1"},
        {"name": "Richard", "address": "Sky st 331"},
        {"name": "Susan", "address": "One way 98"},
        {"name": "Vicky", "address": "Yellow Garden 2"},
        {"name": "Ben", "address": "Park Lane 38"},
        {"name": "William", "address": "Central st 954"},
        {"name": "Chuck", "address": "Main Road 989"},
        {"name": "Viola", "address": "Sideway 1633"}
    ]

    x = mycol.insert_many(mylist)
    print(x.inserted_ids)
    app.run(host="127.0.0.1", port=9872)