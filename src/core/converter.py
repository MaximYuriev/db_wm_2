from typing import Any, Generator

from pandas.core.generic import NDFrame

from src.core.model import Bulletin

type DataFrame = NDFrame


def covert_df_to_model_gen(df: DataFrame) -> Generator[Bulletin, Any, None]:
    for _, row in df.iterrows():
        yield Bulletin.from_df_row(row)
