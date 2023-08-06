kubectl get deployments -n {name-your-service-dashed}
kubectl get services -n {name-your-service-dashed}
kubectl describe service {name-your-service-dashed} -n {name-your-service-dashed}
kubectl get pods -n {name-your-service-dashed}
kubectl logs {name-your-service}-your-pod-id -n {name-your-service-dashed}
kubectl exec -it {name-your-service}-your-pod-id -n {name-your-service-dashed} -- ls /var/log/access_log_{name-your-service}
kubectl describe pod {name-your-service}-your-pod-id -n {name-your-service-dashed}

