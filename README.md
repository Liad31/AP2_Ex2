# # Advanced Programing 2 Exercise 2
This project contains 2 parts.
1. Rest-ful API server which is accessible using HTTP protocol, and provides function for finding anomalies in fligtes to the clients.
2. Web application that uses the server from part 1, so human users can easly find anomalies.

## Usage And Features
You can connect the to the server directly using HTTP protocol, or using the web app. The functions are defined in the execrise.
The web app is easy to use. You can upload a csv file, click on the train button and then on the submit button to start training a new model. The model will apear in the model list in red, once process of learning stopped it will become green, and you will be able the select it, upload another file, select the find anomlies button and then the submit button, and the selected model will look for anomlies. The data is shown on a graph on the left side of the page.
#### Special Features ####
1. When finding anomalies, they will be marked on the graph as red dots, and in the table as red cells.

## Files And Directories
#### Directories
There are 4 main Directories in the project:  
1. templates: There are our HTML files.
2. static: There are our JS and CSS files, images.
3. Main Directory: There are the other directories, and py files (server code)
4. AnomalyDetectionBinaries: There are the anomalyDetection files.
#### Files
The main files are the src code files, like the RestApi.py (server), AnomalyDectetor.py, index.html, mycss.css, main.js (the last 3 for the web page)

## Development
??????????????????????????????

## Installation and Running
#### Installation
???????????????????????????????????????
#### Running
????????????????????????????????????????

## Design
You can see here our [UML diagram](https://online.visual-paradigm.com/app/diagrams/#G1ybPkRMBE0tr0iAb0gHeeCH25_nix_0HF)
#### Rest-ful API server
For the server, we used flask in python. Each respone to a HTTP request is implemented as a method, that the server knows to invoke using the flask.
The server uses code like the graph creator to create graph for the web client, anomaly detection code, and also uses MongoDB as database, to save the models and data about them. Also, the server uses a threadPool to handle requests.
#### Web app
The web app uses the Rest-ful API server in order to handle client's requests interactively. The web browser runs the JS code on the client's side, and when the client request to train or find anomalies, it sends a request to the server.


## Video


