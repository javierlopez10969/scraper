import json
import asyncio
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.book import Book, BookResponse
from app.scraper.buscalibre import BuscalibreScraper
router = APIRouter()

#Best  function to concurrency
@router.post("/book_info")
async def get_info(
    book: Book,
):
    try:
        book = await get_book_info(book)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Sorry our scrapper is down :(, error loading the book.",
        )

    return book