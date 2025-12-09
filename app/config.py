import os

WORKER_URL: str = os.getenv("WORKER_URL", "http://worker-service:8000")
REQUEST_TIMEOUT: float = float(os.getenv("REQUEST_TIMEOUT", "5.0"))
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()