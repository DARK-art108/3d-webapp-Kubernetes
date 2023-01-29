---
title: 7. Connect ToDo with MySQL using ConfigMap and Secret
---

# Lab 7: Connect ToDo with MySQL using ConfigMap and Secret

It is bad practice to store sensitive data, such as passwords, in plain text on a container. However, containers may need this data to perform operations like connecting with other systems. Kubernetes provides an object called Secret that can be used to store sensitive data.

Kubernetes secrets are not really safe, they are base64 encoded, not encrypted. You will need to take additional measures like adding a [Key Management Service](https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/) to your Kubernetes cluster to enhance protection. This would be way out of scope for this tutorial. Commercial Cloud providers typically have out-of-the-box solutions, here is the documentation for [IBM Cloud](https://cloud.ibm.com/docs/containers?topic=containers-encryption&locale=en).

Our example uses the password 'secret' for MySQL. To base64 encode it, you can submit the following command:

```
$ echo -n "secret" | base64
c2VjcmV0
```

- '-n' will prevent a newline character.
- Quotation marks " " are required and not considered part of the password. 
- The result is not a hash, it will always be the same. (A hash would be random.)

This is the definition of our secret ([deploy/secret.yaml](../deploy/secret.yaml)):

```
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
type: Opaque
data:
  password: c2VjcmV0
```

Create it with:

```
kubectl create -f deploy/secret.yaml
```

Using this type of secret is almost the same like using the configmap we created.

This is the relevant section from [deploy/mysql-v4.yaml](../deploy/mysql-v4.yaml):

```
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: password
```

And this is the relevant section from [deploy/todo-v4.yaml](../deploy/todo-v4.yaml):

```
        env:
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: password
```

Apply them as usual:

```
kubectl apply -f deploy/mysql-v4.yaml
kubectl apply -f deploy/todo-v4.yaml
```

Test the app as always. Your previously entered items should still be visible.

---

This concludes our hands-on tutorial. 

You have seen:
* How to deploy applications on Kubernetes using Deployments and Services
* How to expose services with Nodeports
* How to add external storage (to a database) using PersistentVolumes and PersistentVolumeClaims
* How to externalize configuration with ConfigMaps and Secrets

---

**Last Step:** [Kubernetes Dashboard](lab8.md) 




