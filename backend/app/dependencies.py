import os
from typing import Annotated, AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException, Header
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Convert to async URL if needed
if DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

# Async engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=os.getenv("DEBUG", "False").lower() == "true",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    future=True,  # SQLAlchemy 2.0 style
)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for async database sessions"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_and_tables_async():
    """Create database tables (for async engine)"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def get_token_header(x_token: Annotated[str, Header()]) -> str:
    """Validate API token from header"""
    if not TOKEN:
        raise HTTPException(status_code=500, detail="Server not configured properly")
    if x_token != TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return x_token


# Type aliases for cleaner code
TokenDep = Annotated[str, Depends(get_token_header)]
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
