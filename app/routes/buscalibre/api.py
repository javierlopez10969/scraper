from fastapi import APIRouter
from .endpoints import buscalibre

router = APIRouter()
router.include_router(buscalibre.router, tags=["Buscalibre"])
