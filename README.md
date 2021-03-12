# de-twitter-community-grapher
## How to start the backend
* Navigate to the backend folder
* run this line to build the image
```
sudo docker build --tag backend-test .
```
* run this line to spin up the container 
```
sudo docker run -p 5001:5001 backend-test
```

## How to start the frontend
* Navigate to the frontend folder
* run this line to build the image: 
```
sudo docker build --tag frontend-test .
```
* run this line to spin up the container 
```
sudo docker run -p 8080:8080 frontend-test
```
