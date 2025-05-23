import asyncio
from concurrent.futures import ThreadPoolExecutor

from tronpy import Tron
from tronpy.exceptions import AddressNotFound

from core.exceptions import NotFoundError
from tron.schemas import TronResponse


class TronAccount:
    def __init__(self):
        self.client = Tron()
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor()

    async def get_account_info(self, address: str) -> TronResponse:
        try:
            account_balance = await self._get_account_balance(address=address)
            account_resource = await self._get_account_resource(address=address)

            bandwidth = account_resource.get('freeNetLimit', 0)
            energy = account_resource.get('EnergyLimit', 0)

            return TronResponse(
                wallet_address=address,
                balance=account_balance,
                bandwidth=bandwidth,
                energy=energy
            )
        except AddressNotFound:
            raise NotFoundError(f'Address not found: {address}')
        except Exception as ex:
            raise ex

    async def _get_account_balance(self, address: str) -> float:
        return float(await self.loop.run_in_executor(self.executor, self.client.get_account_balance, address))

    async def _get_account_resource(self, address: str) -> dict:
        return await self.loop.run_in_executor(self.executor, self.client.get_account_resource, address)
