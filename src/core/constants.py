BASE_URL = "https://spimex.com/"
URL_FOR_PARSING = BASE_URL + "/markets/oil_products/trades/results/?page=page-"

CONTAINER_CLASS_NAME = "accordeon-inner"
INNER_ELEMENTS_CLASS_NAME = "accordeon-inner__wrap-item"
TITLE_INNER_ELEMENT_CLASS_NAME = "accordeon-inner__item-inner__title"

SEARCHED_TEXT = "Единица измерения: Метрическая тонна"

BULLETIN_HEADER_MAP = {
    "Код\nИнструмента": "exchange_product_id",
    "Наименование\nИнструмента": "exchange_product_name",
    "Базис\nпоставки": "delivery_basis_name",
    "Объем\nДоговоров\nв единицах\nизмерения": "volume",
    "Обьем\nДоговоров,\nруб.": "total",
    "Количество\nДоговоров,\nшт.": "count",
}
