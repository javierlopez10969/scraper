from abc import ABC, abstractmethod
from playwright.async_api._generated import Playwright, Locator
from difflib import SequenceMatcher
from fastapi import HTTPException
import asyncio
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)


class Scraper(ABC):
    def __init__(self, p: Playwright, home_url: str) -> None:
        super().__init__()
        self.home_url = home_url
        self.p = p

    async def init(self) -> bool:
        self.tries = 30
        self.bowser_tries = 3
        self.departmenrtries = 4
        print("Init browser...")
        try:
            self.browser = await self.p.webkit.launch(timeout=20000)
        except Exception:
            raise HTTPException(
                status_code=404,
                detail="Sorry our scrapper is down :(, error launching the browser.",
            )
        self.headers = {
            "Cache-Control": "no-cache",
            "USER-AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            "sec-ch-ua-platform": "macOS",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": None,
        }

        print("Init page...")
        self.page = await self.browser.new_page()
        await self.page.set_extra_http_headers(self.headers)
        print("Going to page...")
        try:
            await self.page.goto(self.home_url, timeout=20000)
        except Exception:
            print("Error loading page, retrying...")
            if self.bowser_tries == 0:
                raise HTTPException(404, "Error loading page")
                return False
                await self.browser.close()
            self.tries = self.bowser_tries - 1
            await self.init()
        return True

    # Waiters
    async def my_own_wait_for_selector(self, selector, time_out):
        try:
            element = await self.page.wait_for_selector(selector, timeout=time_out)
            return element
        except PlaywrightTimeoutError:
            return False

    def similar(self, a: str, b: str):
        return SequenceMatcher(None, a, b).ratio()
