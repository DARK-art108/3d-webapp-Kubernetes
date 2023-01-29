#!/bin/sh
#set -x

echo "----------------------------------------"
echo "URL of the ToDo app:"
echo "http://$(minikube ip):$(kubectl get svc todo --output 'jsonpath={.spec.ports[*].nodePort}')"
echo "----------------------------------------"