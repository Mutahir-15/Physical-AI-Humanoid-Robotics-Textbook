from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/", summary="Health check endpoint")
async def health_check():
    """
    Returns a simple status to indicate the service is running.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ok"}
    )
