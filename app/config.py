import os

WORKER_URL: str = os.getenv("WORKER_URL", "http://worker-service:8000")
REQUEST_TIMEOUT: float = float(os.getenv("REQUEST_TIMEOUT", "5.0"))
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

REDIS_HOST: str = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "60"))