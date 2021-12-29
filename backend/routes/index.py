from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter()


@router.get("/")
async def index() -> RedirectResponse:
    return RedirectResponse(url="/docs")
