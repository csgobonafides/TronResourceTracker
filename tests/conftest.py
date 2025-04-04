import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

import tron.controller.tron_control as tron_modul
from app import app

from core.settings import get_settings, Settings
from db.connector import DatabaseConnector
from tron.clients.tron_account import TronAccount

pytest_plugins = [
    "fixtures.test_db",
    "fixtures.prepare_tron",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest_asyncio.fixture(autouse=True)
async def tron_controller(test_db: DatabaseConnector) -> tron_modul.TronController:
    tron_modul.tron_controller = tron_modul.TronController(db=test_db, tron=TronAccount())
    yield tron_modul.tron_controller


@pytest_asyncio.fixture
async def xclient() -> AsyncClient:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(base_url="http://127.0.0.1:8010", transport=transport) as cli:
        yield cli
