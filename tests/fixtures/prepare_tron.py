from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import WalletInfo


@pytest.fixture
def resource_ids() -> list[UUID]:
    return [uuid4() for _ in range(15)]


@pytest.fixture
def resources(resource_ids: list[UUID]) -> list[WalletInfo]:
    return [WalletInfo(
        resource_id=resource_id,
        wallet_address=f'TWpMnUh9pZS1Mf8yyw9WPiS82WYevKzQo2{i}',
        balance=12323.02 + i,
        bandwidth=400 + i,
        energy=2133 + i
    ) for i, resource_id in enumerate(resource_ids)]


@pytest_asyncio.fixture
async def prepare_tron(test_db: DatabaseConnector, resources: list[WalletInfo]) -> None:
    async with test_db.session_maker(expire_on_commit=False) as session:
        session.add_all(resources)
        await session.commit()
