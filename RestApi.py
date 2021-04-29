import flask
from flask import request,abort
import mysql.connector
import time
import requests
import json
import mysql.connector

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
    mydb = mysql.connector.connect(
        host="localhost",
        user="AP2_EX2",
        password="RestApi"
    )
    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE AP2_EX2")
    app.run(host="127.0.01", port=9872)