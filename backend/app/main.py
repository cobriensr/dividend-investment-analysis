from typing import Union
from datetime import datetime, timezone

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .dependencies import (
    get_async_session,
    get_token_header,
    create_db_and_tables_async,
    AsyncSessionDep,
    TokenDep
)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_db_and_tables_async()
    print("Database tables created")
    yield
    # Shutdown
    print("Shutting down")

# Create FastAPI app
app = FastAPI(
    title="Hero API",
    lifespan=lifespan,
    dependencies=[Depends(get_token_header)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

# Database endpoint test
@app.get("/db-test")
async def test_database(session: AsyncSessionDep):
    """Test database connection with more details"""
    try:
        # Test basic connection
        result = await session.execute(text("SELECT 1 as test"))

        # Test PostgreSQL version
        version_result = await session.execute(text("SELECT version()"))
        version = version_result.scalar()

        # Test current timestamp
        time_result = await session.execute(text("SELECT NOW()"))
        db_time = time_result.scalar()

        return {
            "database": "connected",
            "status": "healthy",
            "test_query": result.scalar(),
            "postgres_version": version,
            "database_time": str(db_time),  # Convert to string
            "api_time": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "database": "error",
            "status": "unhealthy",
            "message": str(e),
            "type": type(e).__name__
        }
