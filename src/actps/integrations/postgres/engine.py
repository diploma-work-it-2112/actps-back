from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.actps.config import POSTGRES_URL

def init_engine(url:str = POSTGRES_URL) -> AsyncEngine:
    async_engine = create_async_engine(
        url=url,
        echo=True,
    )
    return async_engine


async_session = sessionmaker(
    bind=init_engine(), class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    return async_session()

