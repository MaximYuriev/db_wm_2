from typing import Generator

from src.core.model import Bulletin
from src.core.schema import BulletinSchema


def covert_df_to_model_gen(bulletin_schemas_list: list[BulletinSchema]) -> Generator[Bulletin, None, None]:
    for bulletin in bulletin_schemas_list:
        yield bulletin.to_model()
