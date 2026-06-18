### 1. Create the Namespace for ArgoCD

```bash
kubectl create namespace argocd
```

### 2. Install ArgoCD in the created namespace 

```bash
kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 3. Verify the Installation

```bash
kubectl get pods -n argocd
```
Ensure all pods are in `Running` state.


### 4. List All ArgoCD Resources

```bash
kubectl get all -n argocd
```
Ensure all pods show a status of Running before proceeding.
```
NAME                                                   READY   STATUS    RESTARTS    AGE
pod/argocd-application-controller-0                    1/1     Running   0           100m
pod/argocd-applicationset-controller-b7669f646-vm5vr   1/1     Running   0           100m
pod/argocd-dex-server-569b757-z5jnd                    1/1     Running   0           100m
pod/argocd-notifications-controller-58ff87546-kvctw    1/1     Running   0           100m
pod/argocd-redis-b9496d8bf-wxx89                       1/1     Running   0           100m
pod/argocd-repo-server-75ffcfc9df-b6f5h                1/1     Running   0           100m
pod/argocd-server-76755b46f8-x4ppc                     1/1     Running   0           100m
```

### 5. Access the ArgoCD User Interface (UI)
#### 1. Port Forwarding
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

#### 2. Minikube Service
```bash
minikube service argocd-server -n argocd
```

You can then open your browser and navigate to:
```
https://localhost:8080
```

### 6. Log In(Retrieve the Admin Password)ArgoCD
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode; echo
```

### Deploying the ArgoCD Application

#### 1: The Declarative Way (Recommended) argo-application.yaml
```bash
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gitops-argocd-test
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/jdht1992/fastapi-argocd.git
    targetRevision: HEAD
    path: Kubernetes-manifest/fastapi
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd-demo-ns
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
    syncOptions:
      - CreateNamespace=true
```

#### Apply to the Cluster
```bash
kubectl apply -f argo-application.yaml
```


#### 2: The Imperative Way (CLI)
```bash
argocd app create gitops-argocd-test \
  --repo https://github.com/jdht1992/fastapi-argocd.git \
  --revision HEAD \
  --path Kubernetes-manifest/fastapi \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace argocd-demo-ns \
  --project default \
  --sync-policy automated \
  --self-heal \
  --prune \
  --sync-option CreateNamespace=true
```

#### Or use the **Web UI**
1. Applications
1. *+ New App*
2. Fill inputs
6. Create
