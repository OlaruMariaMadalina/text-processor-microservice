from fastapi import FastAPI
import redis
from app.models import TextRequest, AnalysisResult
from app.logging_config import get_logger
from app.config import REDIS_HOST, REDIS_PORT, CACHE_TTL_SECONDS

app = FastAPI()

logger = get_logger("worker-service")
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


@app.post("/analyze", response_model=AnalysisResult)
def analyze(req: TextRequest) -> AnalysisResult:
    """Analyze the input text and return statistics."""
    text = req.text
    logger.info("Analyzing text of length %s", len(text))

    cache_key = f"text-analysis:{text}"

    cached = redis_client.get(cache_key)
    if cached:
        logger.info("Cache hit for text")
        return AnalysisResult.model_validate_json(cached)

    result = AnalysisResult(
        length=len(text),
        word_count=len(text.split()),
        has_numbers=any(ch.isdigit() for ch in text),
        uppercase=text.upper(),
    )

    result_json = result.model_dump_json()
    redis_client.set(cache_key, result_json, ex=CACHE_TTL_SECONDS)

    logger.debug("Stored analysis result in cache: %s", result.model_dump())
    return result


@app.get("/healthz")
async def healthz():
    """Universal health endpoint for both liveness and readiness probes."""
    return {"status": "ok"}
