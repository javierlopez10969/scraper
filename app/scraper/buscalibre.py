from datetime import datetime, timedelta
import time
from playwright.async_api import Playwright
from .scraper import Scraper


class BuscalibreScraper(Scraper):
    def __init__(self, p: Playwright, *args) -> None:
        self.home_url = "https://www.metrogas.cl/pagar-mi-cuenta"
        self.args = args
        self.p = p

    # MetrogasScraper
    async def metrogas(self) -> dict:
        await self.init()
        args = self.args[0]
        address = AddressParser(args["address_street"]).parse_aguas_andinas()
        number = args["address_number"]
        department = "DEP-" + str(args["dep"])
        commune = args["commune"].upper()
        if args["tower"] != None:
            tower = args["tower"]
        else:
            tower = None
        if await self.fillAddress(address, number, department, commune) == False:
            await self.browser.close()
            return {
                "last_pay_date": "0000-00-00",
                "last_pay_amount": "$ 0",
                "actual_consumption": "$ 0",
                "company": "Metrogas",
                "account_number": "0000000-0",
            }
        answer = await self.recolectInformation()
        return answer

    async def fillAddress(self, address, number, dep, commune) -> bool:
        print("Filling address...")
        await self.page.get_by_placeholder("Comuna").nth(0).fill(commune)
        await self.page.locator(
            "xpath = /html/body/div[1]/div/div[1]/div[2]/div/form/div[1]/div[1]/div[2]/ul/li/div"
        ).click(force=True)
        print(address)
        await self.page.get_by_placeholder("Calle").nth(0).fill(address)
        try:
            await self.page.get_by_text(address).click(force=True)
        except Exception:
            print("Error selecting address")
            return False
        await self.page.get_by_placeholder("N°").nth(0).fill(number)
        ##If exists more then 1 element
        number_elementnt = self.page.get_by_text(number)
        answer = await self.my_own_wait_for_selector(
            '//*[@id="__next"]/div/div[1]/div[2]/div/form/div[1]/div[3]/div[2]/ul/li[1]/div',
            2000,
        )
        if answer == False or await number_elementnt.count() > 1:
            return False
        await number_elementnt.click(force=True)
        dep_input = self.page.get_by_placeholder("Casa, Depto, Block")
        await dep_input.fill(dep)
        # await self.page.screenshot(path="screenshots/gas01.png")
        try:
            await self.page.get_by_text(dep, exact=True).click(force=True)
        except Exception:
            print("Error selecting department")
            # await self.page.screenshot(path="screenshots/gas02.png")
            self.departmenrtries = self.departmenrtries - 1
            if self.departmenrtries > 0:
                return await self.fillAddress(address, number, dep, commune)
            return False
        await self.page.get_by_role("button", name="Ingresar").click(force=True)
        return True

    async def recolectInformation(self) -> dict:
        print("Recolecting data...")
        await self.page.wait_for_load_state()
        # await self.page.screenshot(path="screenshots/gas2.png")
        # Find the Information of account
        information = await self.page.locator("div.datos").inner_text()
        information = information.split("\n")
        print(information[3])
        number_account = information[1]
        # Encontrar el septimo h5
        data = await self.page.locator("div.sub-container").inner_text()
        data = data.split(" ")
        last_pay_value = data[4]
        last_pay_date = data[6]
        print(data)
        n = 17
        if len(data) > n:
            if data[17].split("\n")[0].replace(".", "").isdigit() == False:
                actual_consumption = DEFAULT_AMOUNT
            else:
                actual_consumption = "$ " + data[17].split("\n")[0].replace(".", "")
        else:
            actual_consumption = DEFAULT_AMOUNT
        #Special case
        if len(data) == 15:
            due_date = data[2].split("\n")[1]+data[3]+data[4]+data[5]+data[6].split("\n")[0]
            last_pay_date = DEFAULT_DATE
            actual_consumption = "$ "+data[7].split("\n")[0].replace(".", "")
            last_pay_value = "$0"
        if data[2] == 'registra':
            last_pay_date = DEFAULT_DATE
            due_date = DEFAULT_DATE
            last_pay_value = "$0"
        last_pay_date = DateParser(last_pay_date).parse_hyphen()
        due_date = DateParser(due_date).parse_hyphen()
        output = {
            "last_pay_date": last_pay_date ,
            "due_date": due_date,
            "last_pay_amount": last_pay_value.replace("$", "$ ").replace(".", ""),
            "actual_consumption": actual_consumption,
            "previous_consumption": "$ 0",
            "company": "Metrogas",
            "account_number": number_account,
        }
        return output
