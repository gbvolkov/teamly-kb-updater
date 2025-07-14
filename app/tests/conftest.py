# tests/conftest.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture()        # <- default scope = "function"
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
