from flask import Flask,request
import os
import json
import requests
import time
from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback
app = Flask(__name__)

_gremlin_cleanup_graph = "g.V().drop()"

_gremlin_count_vertices = "g.V().count()"

_gremlin_get_all_vertices = "g.V()"

_gremlin_get_follow_edges = "g.E().hasLabel('follows')"

GREMLIN_ENDPOINT = "wss://de-twitter-project.gremlin.cosmos.azure.com:443/"
DATABASE_NAME = "sample-database"
GRAPH_NAME = "meetingtest"
PRIMARY_KEY = "2pHWYzX9IHoMMryHpLEXrmecjKSTrVdcoocpZeR5wHcPixePJnLLITdv0wKTIuzaDRqfmEUYniP7PUuuUgcPsw=="

graph_client = client.Client(f'{GREMLIN_ENDPOINT}', 'g',
                      username=f"/dbs/{DATABASE_NAME}/colls/{GRAPH_NAME}",
                      password=f"{PRIMARY_KEY}",
                      message_serializer=serializer.GraphSONSerializersV2d0()
                      )

@app.route('/')

def auth():
    return os.environ.get("BEARER_TOKEN")

#@app.route('/followers/', methods=['GET'])
def get_followers(username, level, max, parent_id, parent_name):
            print("waiting")
            time.sleep(60)
            url_1 = "https://api.twitter.com/2/users/by?usernames="+username
            params = {"user.fields": "created_at"}
            headers = {"Authorization": "Bearer {}".format(bearer_token)}
            response1 = requests.request("GET", url_1, headers=headers, params = {})
            print(response1.json())
            user_id = response1.json()['data'][0]['id']
            headers = {"Authorization": "Bearer {}".format(bearer_token)}
            url_2 = "https://api.twitter.com/2/users/{}/followers".format(user_id)
            response2 = requests.request("GET", url_2, headers=headers)
            file_json = response2.json()
            
            
            if response2.status_code != 200:
                raise Exception(
                    "Request returned an error: {} {}".format(
                        response2.status_code, response2.text
                    )
                )
            insert_vertices(user_id, username, username)
            if(parent_id != None and parent_name != None):
                # TODO: don't add edge if graph already contains user_id, parent_id connection
                #if getV(parent_id) has outgoing follows edge to user_id
                is_following(parent_id,user_id)
                insert_edges(user_id,parent_id)
            print("Done")
            if(level < max):
                data_json = file_json['data']
                
                for i in data_json:
                    
                    next_name = i['username']
                    if (parent_name != next_name):
                        get_followers(next_name,level+1,max,user_id,username)
            

#            return json.dumps(response.json(), indent=4, sort_keys=True)


def is_following(parent_id, user_id):
    """ Boolean of whether parent is already following child vertex"""
    #TODO: make it return a boolean
    try:
        query = f"g.V('{parent_id}').outE('follows').inV().is('{user_id}')"
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)

        res = ""
        if callback.result() is not None:
            res = callback.result().all().result()
            print("\t Id of edge connecting parent and child:\n\t{0}".format(res))
        else:
            print("Something went wrong with this query: {0}".format(query))
        print("\n")
        print_status_attributes(callback.result())
        print("\n")
        return res

    except GremlinServerError as e:
        print(e)
        error_handler()


#uid: user id, name: any name, username: twitter handle
def insert_vertices(uid, name, username):
    try:
        query = f"g.addV('person').property('id', '{uid}').property('name', '{name}').property('username', '{username}').property('pk','pk')"
        print("\n> {0}\n".format(query))
        callback = graph_client.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this vertex:\n\t{0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(query))
        print("\n")
        print_status_attributes(callback.result())
        print("\n")

    except GremlinServerError as e:
        error_handler()


def print_status_attributes(result):
    # This logs the status attributes returned for successful requests.
    # See list of available response status attributes (headers) that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    #
    # These responses includes total request units charged and total server latency time.
    #
    # IMPORTANT: Make sure to consume ALL results returend by cliient tothe final status attributes
    # for a request. Gremlin result are stream as a sequence of partial response messages
    # where the last response contents the complete status attributes set.
    #
    # This can be
    print("\tResponse status_attributes:\n\t{0}".format(
        result.status_attributes))


def insert_edges(uid1, uid2):
    try:
        query = f"g.V('{uid1}').addE('follows').to(g.V('{uid2}'))"
        print("\n> {0}\n".format(query))
        callback = graph_client.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this edge:\n\t{0}\n".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))
        print_status_attributes(callback.result())
        print("\n")

    except GremlinServerError as e:
        error_handler()


def count_vertices():
    try:
        print("\n> {0}".format(
            _gremlin_count_vertices))
        callback = graph_client.submitAsync(_gremlin_count_vertices)
        if callback.result() is not None:
            print("\tCount of vertices: {0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(
                _gremlin_count_vertices))

        print("\n")
        print_status_attributes(callback.result())

    except GremlinServerError as e:
        error_handler()

def get_vertices(idx = None):
    if(idx == None):
        try:
            query = _gremlin_get_all_vertices
            print("\n> {0}\n".format(query))
            callback = graph_client.submitAsync(query)
            res = ""
            if callback.result() is not None:
                res = callback.result().all().result()
                print("\tGot all vertices:\n\t{0}".format(res))
            else:
                print("Something went wrong with this query: {0}".format(query))
            print("\n")
            print_status_attributes(callback.result())
            print("\n")
            return res

        except GremlinServerError as e:
            error_handler()
    else:
        try:
            query = f"g.V().has('username', unfold().is('{idx}')).emit().repeat(both().dedup()).times(2)"
            print("\n> {0}\n".format(query))
            callback = graph_client.submitAsync(query)
            res = ""
            if callback.result() is not None:
                res = callback.result().all().result()
                print("\tGot vertices:\n\t{0}".format(res))
            else:
                print("Something went wrong with this query: {0}".format(query))
            print("\n")
            print_status_attributes(callback.result())
            print("\n")
            return res

        except GremlinServerError as e:
            error_handler()

def get_edges(idx = None):
    if(idx == None):
        try:
            query = _gremlin_get_follow_edges
            print("\n> {0}\n".format(query))
            callback = graph_client.submitAsync(query)
            res = ""
            if callback.result() is not None:
                res = callback.result().all().result()
                print("\tGot all follows edges:\n\t{0}".format(
                    callback.result().all().result()))
            else:
                print("Something went wrong with this query: {0}".format(query))
            print("\n")
            print_status_attributes(callback.result())
            print("\n")
            for element in res:
                del element['id']
                del element['label']
                del element['type']
                del element['inVLabel']
                del element['outVLabel']
                element['source'] = element['inV']
                del element['inV']
                element['target'] = element['outV']
                del element['outV']
            return res

        except GremlinServerError as e:
            error_handler()
    else:
        try:
            query = f"g.V().has('username', unfold().is('{idx}')).emit().repeat(both().dedup()).times(2).bothE()"
            print("\n> {0}\n".format(query))
            callback = graph_client.submitAsync(query)
            res = ""
            if callback.result() is not None:
                res = callback.result().all().result()
                print("\tGot all follows edges:\n\t{0}".format(
                    callback.result().all().result()))
            else:
                print("Something went wrong with this query: {0}".format(query))
            print("\n")
            print_status_attributes(callback.result())
            print("\n")
            for element in res:
                del element['id']
                del element['label']
                del element['type']
                del element['inVLabel']
                del element['outVLabel']
                element['source'] = element['inV']
                del element['inV']
                element['target'] = element['outV']
                del element['outV']
            return res

        except GremlinServerError as e:
            error_handler()

def get_graph(idx = None):
    if(idx != None):
        try:
            global graph_client
            graph_client = client.Client(f'{GREMLIN_ENDPOINT}', 'g',
                      username=f"/dbs/{DATABASE_NAME}/colls/{idx}",
                      password=f"{PRIMARY_KEY}",
                      message_serializer=serializer.GraphSONSerializersV2d0()
                      )
            
        except GremlinServerError as e:
            error_handler()
    graph = {}
    graph["vertices"] = get_vertices()
    graph["edges"] = get_edges()
    return graph

def error_handler():
    print('Code: {0}, Attributes: {1}'.format(
        e.status_code, e.status_attributes))

    # GremlinServerError.status_code returns the Gremlin protocol status code
    # These are broad status codes which can cover various scenaios, so for more specific
    # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
    #
    # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
    # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
    #
    # See also list of available response status attributes that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    cosmos_status_code = e.status_attributes["x-ms-status-code"]
    if cosmos_status_code == 409:
        print('Conflict error!')
    elif cosmos_status_code == 412:
        print('Precondition error!')
    elif cosmos_status_code == 429:
        print('Throttling error!')
    elif cosmos_status_code == 1009:
        print('Request timeout error!')
    else:
        print("Default error handling")

    traceback.print_exc(file=sys.stdout)
    sys.exit(1)


# if __name__ == "__main__":
#     bearer_token = auth()
#     get_followers("theodonnell77",0,1, None, None)
#     app.run(host='0.0.0.0', port=5001, debug = True)

