from flask import Flask,request
import os
import json
import time
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return "big ole test"

def auth():
    return os.environ.get("BEARER_TOKEN")

@app.route('/followers/', methods=['GET'])
def followers():
    cap = 6 #the maximum number of followers to get (excludes root node).
    collected = 0 #ttl number of follower requests made (excludes root)
    batch_size = 3 #number of requests to try to make at a time
    count = 0 #number of requests made in the batch

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
        if response.status_code == 429:
            time.sleep(60)
        elif response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        else:
            followers = json.dumps(response.json(), indent=4, sort_keys=True)
            follower_dict = json.loads(followers)
            f = open("john_followers.json", "w")
            f.write(followers)
            f.close()

            print(follower_dict['data'])
            for i in range(len(follower_dict['data'])):
                if collected >= cap:
                    break
                follower_id = follower_dict['data'][i]['id']
                follower_username = follower_dict['data'][i]['username']
                # check for rate limit
                follower_url = "https://api.twitter.com/2/users/{}/followers".format(follower_id)
                response = requests.request("GET", follower_url, headers=headers, params=params)
                
                print(response.status_code)
                if response.status_code == 429: #hit rate limit, wait a minute :)
                    time.sleep(60)
                elif response.status_code != 200: #not a success
                    raise Exception(
                    "Request returned an error: {} {}".format(
                        response.status_code, response.text
                    )
                )
                else:
                    followers_follower = json.dumps(response.json(), indent=4, sort_keys=True)
                    f = open(follower_username + ".json", "w")
                    f.write(followers_follower)
                    f.close()

                    count += 1
                    collected += 1
                    if count == batch_size:
                        time.sleep(60*batch_size + 5)
                        count = 0

        return followers
        


# get json
# Option 1: for follower in the json, request then wait one minute. if rate limit exceeded, wait an extra 30 seconds
# Option 2: make 15 requests and wait for 15 mins. then request again, if rate limited, wait another minute or two
# count = 0
# for follower_id in follower_dict["data"][:]["id"]:
# run code from above again
# if response.status_code == rate limit error, status code 429
# wait one more minute, then try again
# store their follower list
# count++
# if count == 15: count = 0 and wait 15 minutes
    
if __name__ == "__main__":
    bearer_token = auth()
    app.run(host='0.0.0.0', port=5001, debug = True)
