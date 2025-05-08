import asyncio

import aiohttp

from src.config import config
from src.core.db import get_async_engine, get_async_session_maker
from src.core.parser import Parser
from src.core.repository import BulletinRepository


async def main():
    async_engine = get_async_engine(config.postgres.db_url)
    session_maker = get_async_session_maker(async_engine)

    async with aiohttp.ClientSession() as session:
        parser = Parser(session)
        df = await parser.get_schemas_from_parsed_website()

    async with session_maker() as db_session:
        repository = BulletinRepository(db_session)
        await repository.add_bulletins_from_df(df)


if __name__ == "__main__":
    asyncio.run(main())
