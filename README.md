## 3d-webapp

A basic 3D static webapp deployed on Kubernetes cluster.

The app has multiple endpoints which you play with. The app is deployed on a Kubernetes cluster and is accessible via a LoadBalancer service.

### Endpoints:

* / - The main page
* health - Health check endpoint
* /score - enpoint which take json input and returns the score json
* /docs - micro doc page
* /meta - meta data of the app

### How to run:

* Clone the repo
* ```docker build --tag ritesh2000/ml-score-api .```
* ```docker run --rm --name test-api -p 5000:5000 -d ritesh2000/ml-score-api```
* ```curl http://localhost:5000/```
* ```docker push ritesh2000/ml-score-api```
* ```docker rm -f test-api``` -- to remove the container(empty port 5000)

After a sucessful test on docker, you can deploy the app on a Kubernetes cluster.

### How to deploy on Kubernetes:

* ```kubectl apply -f kubernetes/namespace.yaml```
* ```kubectl apply -f kubernetes/deployment.yaml```
* ```kubectl apply -f kubernetes/service.yaml```

### How to test:

* ```http://localhost:5000/```  --Test all the endpoints


## todo-sql-app

A dynamic todo app deployed on Kubernetes cluster.

### How to run:

* Clone the repo
* ```kubectl create ns todo``` -- Create a namespace
* ```kubectl apply -f todo-sql-app/deploy/todo-v1.yaml``` -- Deploy the app
* ```stern todo``` -- Check the tail-logs
* ```kubectl port-forward todo-app-7cdfc755c-cq2g2 3000:3000``` -- Forward the port
* ```kubectl apply -f todo-sql-app/deploy/todo-service.yaml```
* ```kubectl get service todo```
* ```kubectl apply -f todo-sql-app/deploy/mysql-v1.yaml``` -- Deploy mysql
* ```stern mysql``` -- Check the tail-logs
* ```kubectl apply -f todo-sql-app/deploy/todo-v2.yaml``` -- Deploy the app with mysql






