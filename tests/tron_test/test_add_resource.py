from decimal import Decimal
from uuid import uuid4

import pytest
from httpx import AsyncClient
from unittest.mock import ANY

from sqlalchemy import select

from db.models import WalletInfo
from db.connector import DatabaseConnector
from tron.schemas.tron import TronResponse
import tron.controller.tron_control as tron_modul


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
