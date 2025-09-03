````markdown
# Instructions for Deploying and Testing ToDo Application on Kubernetes

## 1. Apply All Manifests
All Kubernetes manifests are located in the `.infrastructure` folder.  
To apply them to your cluster, run:

```bash
kubectl apply -f .infrastructure/
````

This will create all necessary Pods, Services, and other resources defined in the manifests.

---

## 2. Test ToDo Application using Port-Forward

The ToDo application listens on port `8000`.
You can access it locally using `kubectl port-forward`:

```bash
kubectl port-forward pod/todoapp 8000:8000
```

Now open your browser and navigate to:

```
http://localhost:8000
```

You should see the ToDo application running.

---

## 3. Test ToDo Application using busyboxplus\:curl

If you want to test connectivity inside the cluster, use the `busyboxplus:curl` pod.

### 3.1 Deploy the busybox pod

```bash
kubectl apply -f .infrastructure/busybox.yml
```

### 3.2 Execute curl from inside the busybox pod

```bash
kubectl exec -it busybox -- sh
```

Inside the pod, run:

```sh
curl http://todoapp:8000
```

* If you used a Service named `todoapp`, the DNS name will resolve to the application Pod.
* Alternatively, you can curl the Pod IP directly:

  ```sh
  curl http://<todoapp_pod_ip>:8000
  ```

To get the Pod IP:

```bash
kubectl get pod todoapp -o wide
```

