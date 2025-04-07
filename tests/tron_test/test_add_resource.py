from decimal import Decimal
import pytest
from httpx import AsyncClient
from unittest.mock import ANY
from sqlalchemy import select

from db.models import WalletInfo
from db.connector import DatabaseConnector
from tron.schemas import TronResponse
import tron.controller as tron_modul


@pytest.mark.asyncio
async def test_add_method(test_db: DatabaseConnector, tron_controller: tron_modul.TronController):
    wallet_info = TronResponse(
        balance = Decimal('172317.09'),
        bandwidth = 760,
        energy = 1233,
        wallet_address = "TUjx6w55Nx9G4GjjRNEB4e7w5BUH3WmJTZ"
    )

    addres = "TUjx6w55Nx9G4GjjRNEB4e7w5BUH3WmJTZ"

    async with test_db.session_maker() as session:
        await tron_controller.add_resource(address=addres, tron_response=wallet_info)

        stmt = select(WalletInfo).filter(WalletInfo.wallet_address == addres)
        result = await session.execute(stmt)
        info_wallet = result.scalars().one_or_none()

        assert info_wallet.balance == wallet_info.balance
        assert info_wallet.bandwidth == wallet_info.bandwidth
        assert info_wallet.energy == wallet_info.energy
        assert info_wallet.wallet_address == addres
        assert info_wallet.resource_id == ANY
        assert info_wallet.create_at == ANY


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_tron")
async def test_add_endpoint_201(xclient: AsyncClient, test_db: DatabaseConnector, resources: WalletInfo):
    '''
    Тест может выдать код ответа 401, нужно попробовать еще раз.
    Это происходит из-за ограничений API Tron.
    '''

    payload = {"address": "TUjx6w55Nx9G4GjjRNEB4e7w5BUH3WmJTZ"}

    response = await xclient.post("/tron/", json=payload)

    assert response.status_code == 201

    response_data = response.json()

    assert "wallet_address" in response_data
    assert "balance" in response_data
    assert "bandwidth" in response_data
    assert "energy" in response_data
    assert "resource_id" in response_data

    assert isinstance(response_data["wallet_address"], str)
    assert isinstance(response_data["balance"], (int, float))
    assert isinstance(response_data["bandwidth"], int)
    assert isinstance(response_data["energy"], int)
    assert isinstance(response_data["resource_id"], str)
