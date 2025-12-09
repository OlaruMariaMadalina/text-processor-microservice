from fastapi import FastAPI
from app.models import TextRequest, AnalysisResult
from app.logging_config import get_logger

app = FastAPI()

logger = get_logger("worker-service")


@app.post("/analyze", response_model=AnalysisResult)
def analyze(req: TextRequest) -> AnalysisResult:
    """Analyze the input text and return statistics."""
    text = req.text
    logger.info("Analyzing text of length %s", len(text))

    result = AnalysisResult(
        length=len(text),
        word_count=len(text.split()),
        has_numbers=any(ch.isdigit() for ch in text),
        uppercase=text.upper(),
    )

    logger.debug("Analysis result: %s", result.model_dump())
    return result
