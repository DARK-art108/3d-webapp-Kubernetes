---
title: 1. Prepare the environment
---

# Lab 1: Prepare the environment

## Get the code

**Note: On bwLehrpool** change into the PERSISTENCE directory before cloning the repository with the following command.

```
git clone https://github.com/Harald-U/kubernetes-handson.git
cd kubernetes-handson
```

## Prepare Minikube

<!-- **NOTE: bwLehrpool** 

> There may be a "leftover" (and damaged) Minikube instance that was present when the VMware image for the Linux environment was built.  This may cause problems. Enter the following command before you start this workshop:

```
minikube delete
```

> Output will be most likely something like this:

```
🔥  minikube" in docker wird gelöscht...
🔥  /home/student/.minikube/machines/minikube wird entfernt...
💀  Removed all traces of the "minikube" cluster.
```

>Please be aware that this command will delete any existing Minikube cluster! -->

**On bwLehrpool or systems with sufficient RAM** start Minikube with this command:

```
minikube start --cpus 2 --memory 6144 --driver docker
```

which will assign 6 GB of RAM.

**On memory constrained systems** use this minimum setup:

```
minikube start --cpus 2 --memory 4096 --driver docker
```

This starts a very small Minikube instance with 2 CPUs and a mere 4 GB of RAM. On Linux and MacOS, Docker is the recommended driver for Minikube. 

---

**Next Step:** [Deploy ToDo stand-alone](lab2.md) 
