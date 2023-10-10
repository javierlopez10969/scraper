from .buscalibre_scraper import BuscalibreScraper


async def scraper_factory(user_type: str, mode: str, *args):

    if mode == "buscalibre":
        return await BuscalibreScraper(*args).buscalibre()
    else:
        raise TypeError("Mode doesn't exist")
