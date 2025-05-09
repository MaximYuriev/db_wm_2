import datetime
from io import BytesIO

from aiohttp import ClientSession
from bs4 import BeautifulSoup, ResultSet, PageElement, Tag, NavigableString

from src.core.constants import URL_FOR_PARSING, BASE_URL, CONTAINER_CLASS_NAME, INNER_ELEMENTS_CLASS_NAME, \
    TITLE_INNER_ELEMENT_CLASS_NAME
from src.core.exceptions import StopDateException
from src.core.parser.schema import BulletinSchema
from src.core.utils.xls_worker import xls_to_schema_list

type HTMLElement = PageElement | Tag | NavigableString
type ParsingResult = ResultSet[HTMLElement]
type xlsFile = BytesIO
type BulletinDate = datetime.date


class Parser:
    def __init__(self, async_http_client: ClientSession):
        self._client = async_http_client

    async def get_schemas_from_parsed_website(self) -> list[BulletinSchema]:
        xls_file_list = await self._get_xls_file_list_from_parsed_site()

        bulletin_schema_list = []
        for xls, date in xls_file_list:
            bulletin_schema_list.extend(xls_to_schema_list(xls, date))

        return bulletin_schema_list

    async def _get_xls_file_list_from_parsed_site(self) -> list[tuple[xlsFile, BulletinDate]]:
        xls_files = []
        for page_number in range(1, 389):
            url = f"{URL_FOR_PARSING}{str(page_number)}"
            response = await self._client.get(url)
            text = await response.text()

            soup = BeautifulSoup(text, 'html.parser')
            elements = self._find_elements(soup)

            try:
                xls_files.extend(await self._find_xls_files(elements))
                print(xls_files)
            except StopDateException:
                return xls_files
        return xls_files

    @staticmethod
    def _find_elements(parser: BeautifulSoup) -> ParsingResult:
        container = parser.find('div', class_=CONTAINER_CLASS_NAME)
        return container.find_all('div', class_=INNER_ELEMENTS_CLASS_NAME)

    async def _find_xls_files(
            self,
            elements: ParsingResult,
            stop_date: datetime.date = datetime.date(2025, 4, 20),
    ) -> list[tuple[xlsFile, BulletinDate]]:
        data_list = []
        for element in elements:
            date = self._get_date(element, stop_date)

            link = element.find('a')['href']

            file_response = await self._client.get(BASE_URL + link)
            excel_data = BytesIO(await file_response.read())
            data_list.append(
                (excel_data, date)
            )

        return data_list

    @staticmethod
    def _get_date(
            element: HTMLElement,
            stop_date: datetime.date,
    ) -> BulletinDate:
        el = element.find(class_=TITLE_INNER_ELEMENT_CLASS_NAME)
        date_text = el.find('span').text
        date = datetime.datetime.strptime(date_text, "%d.%m.%Y").date()
        print(date)
        if date < stop_date:
            raise StopDateException(
                current_date=date,
                stop_date=stop_date,
            )

        return date
