from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    """Request model for input text."""
    text: str = Field(..., min_length=1, max_length=200)


class AnalysisResult(BaseModel):
    """Model for text analysis results."""
    length: int
    word_count: int
    has_numbers: bool
    uppercase: str


class GatewayResponse(BaseModel):
    """Response model for gateway output."""
    input_text: str
    analysis: AnalysisResult
