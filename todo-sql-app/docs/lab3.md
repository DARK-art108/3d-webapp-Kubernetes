---
title: 3. Deploy MySQL
---

# Lab 3: Create MySQL deployment

In the Docker 101 this is the command to start MySQL.

> **Do not run this command!** It is only here for reference.

```
docker run -d \
    --network todo-app --network-alias mysql \
    -v todo-mysql-data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=secret \
    -e MYSQL_DATABASE=todos \
    mysql:8
```

This is the information from the docker command:

* `network` and `network-alias` are not needed in Kubernetes
* Kubernetes has `volumes`, too, but for simplicity we will start without volumes (but add them later)
* The container image name is `mysql:8` (and is implicitely located on Docker Hub)
* There are two `environment variables`, MYSQL_ROOT_PASSWORD and MYSQL_DATABASE

Using this information, the Kubernetes deployment and service configuration for MySQL looks like this ([deploy/mysql-v1.yaml](../deploy/mysql-v1.yaml)):

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: secret
        - name: MYSQL_DATABASE
          value: todos
---
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  selector:
    app: mysql
  type: NodePort
  ports:
    - protocol: TCP
      port: 3306
```

This isn't too different from the todo deployment, the names and labels are changed, and of course the container image reference is different.

> **NOTE:** As you can see, we are creating a Kubernetes Deployment for MySQL. Deployments are typically used for stateless applications which a database like MySQL IS NOT. Stateful applications like a database should use Kubernetes Stateful Sets, instead. What we build here is a demo scenario and for a demo it is sufficient (and easier) to use a Deployment. For a real production MySQL environment with primary and secondary instances and replication you would use a MySQL Kubernetes operator which in turn would most likely result in MySQL StatefulSets. For examples see [Percona Operators](https://www.percona.com/software/percona-kubernetes-operators).

The section for environment variables is new:

```
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: secret
        - name: MYSQL_DATABASE
          value: todos
```

It contains 2 key-value pairs in a YAML array called `env`.

1. Deploy the app and check the logs

    In another, second shell start:
    ```
    stern mysql
    ```

    and in your first shell issue:

    ```
    kubectl apply -f deploy/mysql-v1.yaml
    ```

    There will be a lot of output in the `stern` shell but it should state in the end:

    ```
    mysql-7bf656bfc9-hpn7v mysql 2023-01-11T13:50:06.461633Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections.
    Version: '8.0.31'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
    ```

So MySQL is running in its own pod and waiting for a connection on port 3306 which is MySQL's default.

---

**Next Step:** [Connect ToDo with MySQL using Environment Variables](lab4.md) 