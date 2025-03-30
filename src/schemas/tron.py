from pydantic import BaseModel, UUID4


class TronResponse(BaseModel):
    wallet_address: str
    balance: float
    bandwidth: int
    energy: int


class TronDtlInfo(TronResponse):
    resource_id: UUID4


class TronFullInfo(TronDtlInfo):
    create_at: str
