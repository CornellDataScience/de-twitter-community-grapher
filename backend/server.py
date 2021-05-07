from flask import Flask,request
import os
import json
import time
import requests
from gremlin_handler import *

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def home():
#     format = '''{ "nodes": [
#   { "id": 1, "name": "A" },
#   { "id": 2, "name": "B" }
# ],
# "edges": [
#   { "source": 1, "target": 2 }
# ]}'''
    return "Welcome to the Twitter Grapher API! <br> \
    Available endpoints: <br> \
    GET <br>  \
    /api/graph <br> \
    /api/graph/vertices <br> \
    /api/graph/edges"

@app.route('/api/graph', methods=['GET'])
def vertices_and_edges():
    graph = {}
    if 'account' in request.args:
        id = request.args['account']
        graph["vertices"] = get_vertices(id)
        graph["edges"] = get_edges(id)
    elif 'name' in request.args:
        id = request.args['name']
        print(id)
        graph = get_graph(id)
    else:
        graph["vertices"] = get_vertices()
        graph["edges"] = get_edges()
    for i in graph:
        if i == None:
            print("Item in graph not found")
            return
    return json.dumps(graph)

@app.route('/api/graph/vertices', methods=['GET'])
def vertices():
    vertices = get_vertices()
    if vertices == None:
        print("No vertices found")
        return
    return json.dumps(vertices)

@app.route('/api/graph/edges', methods=['GET'])
def edges():
    edges = get_edges()
    if edges == None:
        print("No edges found")
        return
    return json.dumps(edges)

@app.route('/')
def hello():
    return "big ole test"
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug = True)
