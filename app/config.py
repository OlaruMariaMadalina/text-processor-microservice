import os

WORKER_URL = os.getenv("WORKER_URL", "http://worker-service:8000")

REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "5.0"))