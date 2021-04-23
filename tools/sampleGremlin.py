from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback


_gremlin_cleanup_graph = "g.V().drop()"

_gremlin_count_vertices = "g.V().count()"

client = client.Client('<GREMLIN-ENDPOINT>', 'g',
                       username="/dbs/<DATABASE-NAME>/colls/<GRAPH-NAME>",
                       password="<PRIMARY-KEY>",
                       message_serializer=serializer.GraphSONSerializersV2d0()
                       )


def insert_vertices(uid, name, username):
    try:
        query = f"g.addV('account').property('id', '{uid}').property('name', '{name}').property('username', '{username}').property('pk','pk')"
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
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
        callback = client.submitAsync(query)
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
        callback = client.submitAsync(_gremlin_count_vertices)
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


# try:
#     client = client.Client('wss://de-twitter-project.gremlin.cosmos.azure.com:443/.gremlin.cosmosdb.azure.com:443/', 'g',
#                            username="/dbs/sample-database/colls/test",
#                            password="dDkU9eX4Dxs7oVB9DWcANhDcSsvTwYcpyfoXGSpkik8i5JdryoqliXjd01VuV57IBkyndh3CNsZGjj00S2VuDg==",
#                            message_serializer=serializer.GraphSONSerializersV2d0()
#                            )

    # insert_vertices(client)
    # insert_edges(client)
    # count_vertices(client)

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




# uid, name, username
#insert_vertices(1, "Big Man John", "jodonnell")
#insert_vertices(2, "Big T", "th567")
#insert_vertices(3, "The Boy Aedan", "winter_a")
#insert_vertices(4, "AhadR", "ahad123")
#insert_vertices(5, "TheArjunShah", "arjun127")

#insert_edges("Big Man John","Big T")
#insert_edges("Big Man John","The Boy Aedan")
#insert_edges("Big Man John","AhadR")
#insert_edges("Big Man John","TheArjunShah")
#insert_edges("Big Man John","The Boy Aedan")
#insert_edges("Big T","Big T")
#insert_edges("AhadR","TheArjunShah")
#insert_edges("TheArjunShah","AhadR")

insert_vertices(6, "hahatest", "test")
insert_edges(1,6)

count_vertices()