import fastapi
import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI

from main import create_app


@pytest_asyncio.fixture
async def application() -> fastapi.FastAPI:
    return create_app()


@pytest_asyncio.fixture
async def http_client(application: FastAPI) -> httpx.AsyncClient:
    async with LifespanManager(application):
        async with httpx.AsyncClient(app=application, base_url='http://testserver') as client:
            yield client
            await client.aclose()


class TestCreateShoeAcceptance:

    @pytest.mark.asyncio
    async def test_create_one_shoe_success(self, http_client: httpx.AsyncClient):
        response = await http_client.post(url='/v1/shoes', json={'name': 'Adidas Predator 2024'})
        assert response.status_code == 204
