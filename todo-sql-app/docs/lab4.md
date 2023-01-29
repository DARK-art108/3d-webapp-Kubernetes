---
title: 4. Connect ToDo with MySQL using Environment Variables
---

# Lab 4: Connect ToDo with MySQL using Environment Variables


This is the docker command from Docker 101 that will connect the ToDo app with MySQL.

> Again: **Do not run this command!**

```
docker run -dp 3000:3000 \
  --name todo \
  --network todo-app \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  todo-app
```

* `network` is not used and needed in Kubernetes
* There are now 4 environment variables that we will use

Our deployment and service configuration looks like this now ([deploy/todo-v2.yaml](../deploy/todo-v2.yaml)):

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-app
  labels:
    app: todo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo
  template:
    metadata:
      labels:
        app: todo
    spec:
      containers:
      - name: todo
        image: haraldu/todo-app:latest
        ports:
        - containerPort: 3000
        env:
        - name: MYSQL_PASSWORD
          value: secret
        - name: MYSQL_DB
          value: todos
        - name: MYSQL_HOST
          value: mysql
        - name: MYSQL_USER
          value: root
---
apiVersion: v1
kind: Service
metadata:
  name: todo
spec:
  selector:
    app: todo
  type: NodePort
  ports:
    - protocol: TCP
      port: 3000
```

All that changed from `deploy/todo-v1.yaml` was to add the environment variables (`env:` section).

But how will the ToDo app find the MySQL server/pod? The environment variable MYSQL_HOST seems a good pick but it contains only 'mysql'. How is this going to work?

When we created the MySQL Kubernetes service definition with the name 'mysql', this name 'mysql' was registered with the Kubernetes DNS (name service). Our two pods and two services share the same [Kubernetes namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) ("default") and therefore the MySQL service doesn't need any further qualification. Apps in the same namespace can simply call other apps or send requests to them using their service's name only. Apps in different namespaces can use the fully qualified name: [servicename].[namespacename].cloud.local (e.g. `mysql.default.cloud.local`). 

1. Deploy the configuration to Kubernetes

    Reuse the second shell but redirect `stern` to the Todo app:

    ```
    stern todo
    ```

    Then, in the first shell, deploy the new Todo version:

    ```
    kubectl apply -f deploy/todo-v2.yaml
    ```

    `stern` output shows:

    ```
    + todo-app-f8549b989-hhvj6 › todo
    todo-app-f8549b989-hhvj6 todo Using sqlite database at /etc/todos/todo.db
    todo-app-f8549b989-hhvj6 todo Listening on port 3000
    + todo-app-744bcb9777-vjl7c › todo
    todo-app-744bcb9777-vjl7c todo Waiting for mysql:3306.
    todo-app-744bcb9777-vjl7c todo Connected!
    todo-app-744bcb9777-vjl7c todo Connected to mysql db at host mysql
    todo-app-744bcb9777-vjl7c todo Listening on port 3000
    - todo-app-f8549b989-hhvj6
    ```

    The first pod, todo-app-f8549b989-hhvj6, was connected to sqlite. 
    A new pod, todo-app-744bcb9777-vjl7c, is started (indicated by '+') and successfully connects to MySQL.
    The last message (preceded with '-') indicates that the first pod, todo-app-f8549b989-hhvj6, has terminated.

    > With the configuration file todo-v2.yaml you "declared a new intent" regarding the state of the Todo app and by "apply"ing it, you made this known to Kubernetes. Kubernetes then changed the existing state of the Todo application to match the desired state by starting a new pod and deleting the old one. This approach is called "declarative". 
    > With Docker, you used an "imperative" approach: tell Docker to stop the old container ("docker stop ..."), then delete the old container ("docker rm ..."), then start the new container ("docker run ..."). 


2. Test the app in your browser 

    ```
    minikube service todo
    ```

    Make sure to add some items!

---

**Next Step:** [MySQL with Persistent Volumes](lab5.md) 