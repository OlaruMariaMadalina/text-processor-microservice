from fastapi import FastAPI, HTTPException
import httpx
from app.models import TextRequest, GatewayResponse, AnalysisResult
from app.config import WORKER_URL, REQUEST_TIMEOUT

app = FastAPI()


@app.post("/process-text", response_model=GatewayResponse)
async def process_text(req: TextRequest) -> GatewayResponse:
    """Send input text to worker service and return analysis result."""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            resp = await client.post(
                f"{WORKER_URL}/analyze",
                json=req.model_dump(),
            )
            resp.raise_for_status()

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Worker network error: {e}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Worker error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {e}"
        )

    data = resp.json()
    analysis = AnalysisResult(**data)

    gateway_response = GatewayResponse(
        input_text=req.text,
        analysis=analysis,
    )

    return gateway_response
