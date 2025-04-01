import pytest
import pytest_asyncio
from httpx import AsyncClient

import tron.controller.tron_control as tron_modul
from app import app

from core.settings import get_settings, Settings
from db.connector import DatabaseConnector

pytest_plugins = [
    "fixtures.test_db",
    "fixtures.prepare_tron",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest_asyncio.fixture(autouse=True)
async def tron_controller(test_db: DatabaseConnector) -> tron_modul.TronController:
    tron_modul.tron_controller = tron_modul.TronController(test_db)
    yield tron_modul.tron_controller


@pytest_asyncio.fixture
async def xclient() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8010") as cli:
        yield cli
