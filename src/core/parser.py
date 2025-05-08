import datetime
from io import BytesIO

import pandas as pd
import xlrd
from aiohttp import ClientSession
from bs4 import BeautifulSoup, ResultSet, PageElement, Tag, NavigableString
from pandas.core.generic import NDFrame

from src.core.constants import URL_FOR_PARSING, BASE_URL, CONTAINER_CLASS_NAME, INNER_ELEMENTS_CLASS_NAME, \
    TITLE_INNER_ELEMENT_CLASS_NAME, SEARCHED_TEXT, BULLETIN_HEADER_MAP
from src.core.exceptions import StopDateException

type HTMLElement = PageElement | Tag | NavigableString
type ParsingResult = ResultSet[HTMLElement]
type xlsFile = BytesIO
type DataFrame = NDFrame
type BulletinDate = datetime.date


class Parser:
    def __init__(self, async_http_client: ClientSession):
        self._client = async_http_client

    async def get_df_from_parsed_website(self) -> DataFrame:
        xls_file_list = await self._get_xls_file_list_from_parsed_site()
        df_list = [self._xls_to_df(xls, date) for xls, date in xls_file_list]

        df = pd.concat(
            df_list,
            ignore_index=True,
        )

        return df

    async def _get_xls_file_list_from_parsed_site(self) -> list[tuple[xlsFile, BulletinDate]]:
        page_number = 1
        xls_files = []
        while True:
            _url = f"{URL_FOR_PARSING}{str(page_number)}"
            response = await self._client.get(_url)
            text = await response.text()

            soup = BeautifulSoup(text, 'html.parser')
            elements = self._find_elements(soup)

            try:
                xls_files.extend(await self._find_xls_files(elements))
            except StopDateException:
                return xls_files

            page_number += 1

    @staticmethod
    def _find_elements(parser: BeautifulSoup) -> ParsingResult:
        container = parser.find('div', class_=CONTAINER_CLASS_NAME)
        return container.find_all('div', class_=INNER_ELEMENTS_CLASS_NAME)

    async def _find_xls_files(
            self,
            elements: ParsingResult,
            stop_date: datetime.date = datetime.date(2023, 1, 1),
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

        if date < stop_date:
            raise StopDateException(
                current_date=date,
                stop_date=stop_date,
            )

        return date

    @staticmethod
    def _xls_to_df(
            xls_file: xlsFile,
            date: datetime.date,
    ) -> DataFrame:
        workbook = xlrd.open_workbook(file_contents=xls_file.read())
        sheet = workbook.sheet_by_index(0)

        start_row = 0
        search_text = SEARCHED_TEXT
        for row_idx in range(sheet.nrows):
            row_values = sheet.row_values(row_idx)
            if any(search_text in str(cell) for cell in row_values):
                start_row = row_idx + 1

        df = pd.read_excel(xls_file, skiprows=start_row, engine="xlrd")
        df = df[
            [header for header in BULLETIN_HEADER_MAP.keys()]
        ].rename(columns=BULLETIN_HEADER_MAP).replace('-', None).dropna()
        df["date"] = date
        return df
