import pytest
from httpx import AsyncClient

from db.models import WalletInfo


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_tron")
async def test_get_resource(xclient: AsyncClient, resource: WalletInfo):

    response = await xclient.get("/tron/?page=2&page_size=5")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 5

    for item in data:
        assert item == {
            "resource_id": resource.resource_id,
            "wallet_address": resource.wallet_address,
            "balance": resource.balance,
            "bandwidth": resource.bandwidth,
            "energy": resource.energy
        }
