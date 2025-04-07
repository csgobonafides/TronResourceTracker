import uuid
from sqlalchemy import select

from core.exceptions import BadRequestError
from db.connector import DatabaseConnector
from db.models import WalletInfo
from tron.tron_client import TronAccount
from tron.schemas import TronDtlInfo, TronFullInfo, TronResponse


class TronController:

    def __init__(self, db: DatabaseConnector, tron: TronAccount):
        self.db = db
        self.tron = tron


    async def check_and_add_resource(self, address: str) -> TronDtlInfo:
        tron_resource = await self.get_account_information(address=address)
        return await self.add_resource(address=address, tron_response=tron_resource)


    async def get_account_information(self, address: str) -> TronResponse:
        return await self.tron.get_account_info(address=address)


    async def add_resource(self, address: str, tron_response: TronResponse) -> TronDtlInfo:

        resource_id = uuid.uuid4()

        async with self.db.session_maker() as session:
            try:
                trn = WalletInfo(
                    resource_id=resource_id,
                    wallet_address=address,
                    balance=tron_response.balance,
                    bandwidth=tron_response.bandwidth,
                    energy=tron_response.energy
                )
                session.add(trn)
                await session.commit()
            except Exception as ex:
                raise ex
        return TronDtlInfo(
            resource_id=resource_id,
            wallet_address=address,
            balance=tron_response.balance,
            bandwidth=tron_response.bandwidth,
            energy=tron_response.energy
        )


    async def get_resource(self, page: int = 1, page_size: int = 5) -> list[TronFullInfo]:
        async with self.db.session_maker() as session:
            try:
                offset = (page - 1) * page_size

                query = await session.execute(select(WalletInfo).offset(offset).limit(page_size))
                results = query.scalars().all()

                resources = [
                    TronFullInfo(
                        resource_id=record.resource_id,
                        wallet_address=record.wallet_address,
                        balance=record.balance,
                        bandwidth=record.bandwidth,
                        energy=record.energy,
                        create_at=str(record.create_at),
                    )
                    for record in results
                ]
                return resources
            except Exception as ex:
                raise ex


tron_controller: TronController = None


def get_controller() -> TronController:
    if tron_controller is None:
        raise BadRequestError("Controller is none.")
    return tron_controller
