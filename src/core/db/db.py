from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.core.parser.schema import BulletinSchema


def get_async_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url, echo=False)


def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def save_bulletin_in_db(session: AsyncSession, bulletin_schema_list: list[BulletinSchema]) -> None:
    model_gen = (bulletin_schema.to_model() for bulletin_schema in bulletin_schema_list)
    model_list = []

    for model in model_gen:
        if len(model_list) == 500:
            session.add_all(model_list)
            model_list.clear()
        else:
            model_list.append(model)

    if len(model_list) != 0:
        session.add_all(model_list)

    await session.commit()
