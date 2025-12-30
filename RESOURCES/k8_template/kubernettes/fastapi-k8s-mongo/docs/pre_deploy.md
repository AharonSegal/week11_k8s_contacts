# Pre-Deployment Kubernetes Checklist for FastAPI + MongoDB (Windows)

if on
    minikube status
     minikube test status
else
    minikube start
    or give name 
    minikube start -p dev
    minikube start -p test

minikube profile list

minikube profile test
minikube profile minikube

---

kubectl config current-context


minikube profile list
kubectl config current-context
kubectl get nodes

minikube delete -p minikube


## 1️⃣ Check if `kubectl` is installed

```bash
kubectl version --client
````
