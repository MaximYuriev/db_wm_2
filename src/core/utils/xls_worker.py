import datetime
from io import BytesIO

import xlrd

from src.core.constants import END_REPORT_FILE_ROW, SEARCHED_TEXT
from src.core.exceptions import TableNotFoundException
from src.core.schema import BulletinSchema
from src.core.utils.headers import BulletinHeaderEnum

type xlsFile = BytesIO
type StartTableIndex = int
type HeaderName = str
type CellIndex = int


class XLSWorker:
    def __init__(self, xls_file: xlsFile, date: datetime.date):
        self._workbook = xlrd.open_workbook(file_contents=xls_file.read())
        self._bulletin_date = date
        self._sheet = self._workbook.sheet_by_index(0)
        self._table_idx = self._find_table_idx(table_title=SEARCHED_TEXT)
        self._table_headers = self._get_table_headers()

    def xls_to_schema_list(
            self,
    ) -> list[BulletinSchema]:
        bulletin_list = []
        for row_idx in range(self._table_idx + 2, self._sheet.nrows):
            row_values = self._sheet.row_values(row_idx)
            exchange_product_id = row_values[self._table_headers[BulletinHeaderEnum.EXCHANGE_PRODUCT_ID]]

            if exchange_product_id not in END_REPORT_FILE_ROW:
                bulletin = BulletinSchema(
                    exchange_product_id=exchange_product_id,
                    exchange_product_name=row_values[self._table_headers[BulletinHeaderEnum.EXCHANGE_PRODUCT_NAME]],
                    delivery_basis_name=row_values[self._table_headers[BulletinHeaderEnum.DELIVERY_BASIS_NAME]],
                    volume=row_values[self._table_headers[BulletinHeaderEnum.VOLUME]],
                    total=row_values[self._table_headers[BulletinHeaderEnum.TOTAL]],
                    count=row_values[self._table_headers[BulletinHeaderEnum.COUNT]],
                    date=self._bulletin_date,
                )
                if bulletin.count > 0:
                    bulletin_list.append(bulletin)

        return bulletin_list

    def _find_table_idx(self, table_title: str) -> StartTableIndex:
        for row_idx in range(self._sheet.nrows):
            row_values = self._sheet.row_values(row_idx)
            if any(table_title in str(cell) for cell in row_values):
                return row_idx + 1
        raise TableNotFoundException(table_title)

    def _get_table_headers(self) -> dict[BulletinHeaderEnum, CellIndex]:
        row = self._sheet.row_values(self._table_idx)
        header_map = {}

        for idx, header in enumerate(row):
            normalized_header = header.lower().replace("\n", " ")
            if normalized_header in BulletinHeaderEnum:
                header_map[BulletinHeaderEnum(normalized_header)] = idx

        return header_map
