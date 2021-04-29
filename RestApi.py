import flask
from flask import request,abort
import mysql.connector
import time
import requests
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
    print(request.form)
    #print(request.get_json())
    return "hi"





























if __name__ == "__main__":
    app.run(host="127.0.01", port=9876)