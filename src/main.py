import asyncio

import aiohttp

from src.config import config
from src.core.db.db import get_async_engine, get_async_session_maker, save_bulletin_in_db
from src.core.parser.parser import Parser


async def main():
    async_engine = get_async_engine(config.postgres.db_url)
    session_maker = get_async_session_maker(async_engine)

    async with aiohttp.ClientSession() as session:
        parser = Parser(session)
        bulletin_schema_list = await parser.get_schemas_from_parsed_website()

    async with session_maker() as db_session:
        await save_bulletin_in_db(session=db_session, bulletin_schema_list=bulletin_schema_list)


if __name__ == "__main__":
    asyncio.run(main())
