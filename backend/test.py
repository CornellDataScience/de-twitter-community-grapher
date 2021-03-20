from flask import Flask,request
import os
import json
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return "big ole test"

def auth():
    return os.environ.get("BEARER_TOKEN")

@app.route('/followers/', methods=['GET'])
def followers():
    if 'username' in request.args:
        id = request.args['username']
        url_1 = "https://api.twitter.com/2/users/by?usernames="+id
        params = {"user.fields": "created_at"}
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        response = requests.request("GET", url_1, headers=headers, params = {})
        print(response.json())
        user_id = response.json()['data'][0]['id']
        url_2 = "https://api.twitter.com/2/users/{}/followers".format(user_id)
        response = requests.request("GET", url_2, headers=headers, params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return json.dumps(response.json(), indent=4, sort_keys=True)
    
if __name__ == "__main__":
    bearer_token = auth()
    app.run(host='0.0.0.0', port=5001, debug = True)
