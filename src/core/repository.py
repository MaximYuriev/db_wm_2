from pandas.core.generic import NDFrame
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.converter import covert_df_to_model_gen

type DataFrame = NDFrame


class BulletinRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_bulletins_from_df(self, df: DataFrame):
        model_gen = covert_df_to_model_gen(df)

        for model in model_gen:
            self._session.add(model)

        await self._session.commit()
