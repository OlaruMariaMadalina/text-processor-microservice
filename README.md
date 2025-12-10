# Text Processor Microservice

This project implements a microservices-based text processing system using FastAPI, Redis for caching, Docker for containerization, and Kubernetes (Minikube) for orchestration.

It demonstrates service-to-service communication, caching, environment-driven configuration via ConfigMaps, readiness/liveness probes, horizontal scaling, Ingress-based routing, and resource monitoring through the Kubernetes metrics server.

## Architecture Overview

```
Client → Ingress → API Gateway → Worker Service → Redis
```

- **API Gateway** (`app/api_gateway.py`): Exposes the main `/process-text` endpoint for external clients.
- **Worker Service** (`app/worker_service.py`): Processes text tasks, uses Redis for caching and queueing.
- **Redis**: Stores processed results and pending tasks.
- **ConfigMap**: Controls log level and service URLs.
- **Probes**: `/healthz` endpoint for liveness and readiness checks.

## Configuration & Environment Variables

- `WORKER_URL`: URL for the worker service (used by API Gateway)
- `REQUEST_TIMEOUT`: Timeout (seconds) for requests to the worker
- `LOG_LEVEL`: Logging level for all services
- `REDIS_HOST`: Redis hostname or service name
- `REDIS_PORT`: Redis port
- `CACHE_TTL_SECONDS`: Time-to-live for cached results in Redis (seconds)

## Running the system

1. **Start Minikube (inside Ubuntu/WSL)**
    ```sh
    minikube start --driver=docker
    eval $(minikube docker-env)
    ```
2. **Build Docker Image**
    ```sh
    docker build -t text-processor:dev .
    ```
3. **Apply kubernetes manifests**
    ```sh
    kubectl apply -f k8s/redis.yaml
    kubectl apply -f k8s/configmap.yaml
    kubectl apply -f k8s/api-deployment.yaml
    kubectl apply -f k8s/worker-deployment.yaml
    kubectl apply -f k8s/ingress.yaml
    ```
4. **Verify Deployments**
    ```sh
    kubectl get pods
    kubectl get svc
    kubectl get ingress
    ```

## Key Files Explained

- `app/api_gateway.py`: Defines the `/process-text` endpoint, receives requests and forwards them to the worker.
- `app/worker_service.py`: Processes text, uses Redis for caching/queueing, exposes `/analyze`.
- `k8s/redis.yaml`: Redis deployment and service.
- `k8s/api-deployment.yaml`, `k8s/worker-deployment.yaml`: Deployments for API Gateway and Worker.
- `k8s/configmap.yaml`: Configuration variables (e.g., log level).
- `k8s/ingress.yaml`: External access configuration for API Gateway.

## Testing the Microservice

### Using Ingress

1. **Test Health Endpoint:**
    ```sh
    curl http://<minikube-ip>/healthz
    ```

2. **Process Text:**
    ```sh
    curl -X POST http://<minikube-ip>/process-text \
      -H "Content-Type: application/json" \
      -d '{"text": "hello ingress"}'
    ```

---

### Using `kubectl port-forward` (Alternative)

1. **Port Forward API Gateway:**
    ```sh
    kubectl port-forward deployment/api-gateway-deployment 8000:8000
    ```

2. **Test Endpoints:**
    ```sh
    curl http://localhost:8000/healthz
    curl http://localhost:8000/process-text
    ```

---

### Metrics and Resource Observation

1. **Enable Metrics Server:**
    ```sh
    minikube addons enable metrics-server
    ```

2. **Check Pod and Node Usage:**
    ```sh
    kubectl top pods
    kubectl top nodes
    ```

    **Example Output:**
    ```
    NAME           CPU(cores)   MEMORY(bytes)
    api-gateway    2m           80Mi
    worker         2m           60Mi
    redis          4m           3Mi
    ```