---
title: 6. Connect ToDo with MySQL using ConfigMap
---

# Lab 6: Connect ToDo with MySQL using ConfigMap

Both, ToDo and MySQL use environment variables.

- mysql:
  - MYSQL_ROOT_PASSWORD = secret
  - MYSQL_DATABASE =todos
- todo:
  - MYSQL_PASSWORD = secret
  - MYSQL_DB = todos
  - MYSQL_HOST = mysql
  - MYSQL_USER = root

Two of them serve identical purposes, password and database, but are named differently.

Configuration parameters like these should be stored externally **(-> 12-Factor Apps!)** in [Kubernetes ConfigMaps](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/). 

There are different ways to create a configmap. We use a simple version for our purpose which looks like this ([deploy/configmap-v1.yaml](../deploy/configmap-v1.yaml)):

```
kind: ConfigMap
apiVersion: v1
metadata:
  name: mysql-config
  labels:
    app: todo  
data:
  MYSQL_PASSWORD: "secret"
  MYSQL_DB: "todos"
  MYSQL_HOST: "mysql"
  MYSQL_USER: "root"
```

It has a name, mysql-config, and in the data array are for key value pairs. I used the variable names that the ToDo app requires, but in fact they could be anything meaningful.

In the Kubernetes deployment configuration, the config map is used in the environment area. 

This is the old version, using environment variables:

```
env:
- name: MYSQL_PASSWORD
  value: secret
```           

And this is an example referencing a config map:

```
env:
- name: MYSQL_PASSWORD
    valueFrom:
    configMapKeyRef:
        name: mysql-config
        key: MYSQL_PASSWORD
```

The ToDo configuration is this ([deploy/todo-v3.yaml](../deploy/todo-v3.yaml)):

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
          valueFrom:
            configMapKeyRef:
              name: mysql-config
              key: MYSQL_PASSWORD
        - name: MYSQL_DB
          valueFrom:
            configMapKeyRef:
              name: mysql-config
              key: MYSQL_DB
        - name: MYSQL_HOST
          valueFrom:
            configMapKeyRef:
              name: mysql-config
              key: MYSQL_HOST
        - name: MYSQL_USER
          valueFrom:
            configMapKeyRef:
              name: mysql-config
              key: MYSQL_USER
---
```

The MySQL configuration is this ([deploy/mysql-v3.yaml](../deploy/mysql-v2.yaml)):

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
  labels:
    app: mysql
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
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
        image: mysql:5.7
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            configMapKeyRef:
              name: mysql-config
              key: MYSQL_PASSWORD
        - name: MYSQL_DATABASE
          valueFrom:
            configMapKeyRef:
              name: mysql-config
              key: MYSQL_DB
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: mysql-pv-claim                    
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
    - port: 3306
```

Notice that we read e.g. MYSQL_PASSWORD from the configmap but assign it to MYSQL_ROOT_PASSWORD.

1. Create the ConfigMap:

    ```
    kubectl create -f deploy/configmap-v1.yaml
    ```

    **Note:** For a ConfigMap use `create` instead of `apply` as `kubectl` command. They have no "desired" state. If you need to change a ConfigMap, you delete and recreate it. 

2. Apply the new MySQL configuration:

    ```
    kubectl apply -f deploy/mysql-v3.yaml
    ```
   
   Actually this will not change anything since the content of the variables is only used during initial startup when the MySQL setup is performed.

3. Apply the new ToDo configuration:
    ```
    kubectl apply -f deploy/todo-v3.yaml
    ```

4. Test the app. You should see your previous items still there.

---

**Next Step:** [Connect ToDo with MySQL using ConfigMap and Secret](lab7.md) 

