from fastapi import FastAPI
from app.models import TextRequest, AnalysisResult

app = FastAPI()


@app.post("/analyze", response_model=AnalysisResult)
def analyze(req: TextRequest) -> AnalysisResult:
    """Analyze the input text and return statistics."""
    text = req.text

    result = AnalysisResult(
        length=len(text),
        word_count=len(text.split()),
        has_numbers=any(ch.isdigit() for ch in text),
        uppercase=text.upper(),
    )

    return result
