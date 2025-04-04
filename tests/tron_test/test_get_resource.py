import pytest
from httpx import AsyncClient
from unittest.mock import ANY

from db.models import WalletInfo


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_tron")
async def test_get_resource_5_10(xclient: AsyncClient, resources: list[WalletInfo]):

    response = await xclient.get("/tron/?page=2&page_size=5")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 5

    assert data == [
        {
            "balance": resource.balance,
            "bandwidth": resource.bandwidth,
            "energy": resource.energy,
            "resource_id": str(resource.resource_id),
            "wallet_address": resource.wallet_address,
            "create_at": ANY
        }
        for resource in resources[5:10]
    ]


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_tron")
async def test_get_resource_10_14(xclient: AsyncClient, resources: list[WalletInfo]):

    response = await xclient.get("/tron/?page=3&page_size=5")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 4

    assert data == [
        {
            "balance": resource.balance,
            "bandwidth": resource.bandwidth,
            "energy": resource.energy,
            "resource_id": str(resource.resource_id),
            "wallet_address": resource.wallet_address,
            "create_at": ANY
        }
        for resource in resources[10:14]
    ]
