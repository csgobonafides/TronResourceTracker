from decimal import Decimal
from pydantic import BaseModel, UUID4
from typing import Optional, Union


class TronResponse(BaseModel):
    wallet_address: str
    balance: Optional[Union[float, Decimal]] = 0
    bandwidth: Optional[int] = 0
    energy: Optional[int] = 0


class TronDtlInfo(TronResponse):
    resource_id: UUID4


class TronFullInfo(TronDtlInfo):
    create_at: str


class TronRequest(BaseModel):
    address: str
