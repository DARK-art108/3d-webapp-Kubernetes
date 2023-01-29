---
title: 5. MySQL with Persistent Volumes
---

# Lab 5: MySQL with Persistent Volumes

Our initial MySQL deployment in Lab 2 has no external storage, instead it stores data on the filesystem within the pod. This doesn't really make sense for a database: When the pod is recreated for any reason, the data is gone!

Kubernetes has a method to create external storage using two object types: PersistentVolumes and PersistentVolumeClaims. This is their definition in the Kubernetes docs:

_A [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) (PV) is a piece of storage in the cluster that has been manually provisioned by an administrator, or dynamically provisioned by Kubernetes using a [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes)._

_A [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) (PVC) is a request for storage by a user that can be fulfilled by a PV._ 

_PersistentVolumes and PersistentVolumeClaims are **independent from Pod lifecycles and preserve data through restarting, rescheduling, and even deleting Pods**._

Minikube has one built-in StorageClass of type [HostPath](https://minikube.sigs.k8s.io/docs/handbook/persistent_volumes/). It will dynamically create the PersistentVolume (PV) for every new PersistentVolumeClaim (PVC).

The new Kubernetes configuration is in [deploy/mysql-v2.yaml](../deploy/mysql-v2.yaml). It contains a new section for the PersistentVolumeClaim (PVC):

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
```

In Kubernetes there are 3 possible accessModes:

- ReadWriteOnce -- the volume can be mounted as read-write by a single node
- ReadOnlyMany -- the volume can be mounted read-only by many nodes
- ReadWriteMany -- the volume can be mounted as read-write by many nodes

The Minikube storage class HostPath only supports ReadWriteOnce.

In our example, 1 GB of storage is requested.

The new deployment configuration looks like this:

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
        image: mysql:5.7
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: secret
        - name: MYSQL_DATABASE
          value: todos
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: mysql-pv-claim
```

* There is a new 'volumes' section that maps the PVC to a name in the deployment.
* The 'containers' definition mounts a path within the pod (/var/lib/mysql) onto that PVC. 

When the pod is started for the first time, a claim is made for storage and Kubernetes/Minikube tries to satisfy this claim by creating a PV. If it cannot create the PV -- maybe there is no more storage available -- the pod will not start.

1. Redeploy MySQL:

    ```
    kubectl apply -f deploy/mysql-v2.yaml
    ```

2. Check if the PVC has been created:

    ```
    kubectl get pvc

    NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
    mysql-pv-claim   Bound    pvc-ba7114e0-ad6a-4427-8814-3c3f681c94b0   1Gi        RWO            standard       7m16s
    ```

3. Check if the PV has been created:

    ```
    kubectl get pv

    NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                    STORAGECLASS   REASON   AGE
    pvc-ba7114e0-ad6a-4427-8814-3c3f681c94b0   1Gi        RWO            Delete           Bound    default/mysql-pv-claim   standard                8m57s
    ```

4. If you refresh the ToDo app in the browser, it may have lost connection with MySQL. If this happened, we need to restart the pod to force a new connection. 

    There is no "restart" for Pods, the solution is to delete the Pod and have Kubernetes recreate it:

    ```
    kubectl get pod

    NAME                        READY   STATUS    RESTARTS   AGE
    mysql-5bfb9886b6-j2c8h      1/1     Running   0          67s
    todo-app-744bcb9777-v8v64   1/1     Running   0          2m20s
    ```

    ```
    kubectl delete pod todo-app-744bcb9777-v8v64

    pod "todo-app-744bcb9777-v8v64" deleted
    ```

    > The name of your todo pod will be different, of course!

5. Test the app. 
   
   If you closed your browser, reopen the ToDo app with

    ```
    minikube service todo
    ```

    There will be no items, make sure to add some new ones.


---

**Next Step:** [Connect ToDo with MySQL using ConfigMap](lab6.md) 