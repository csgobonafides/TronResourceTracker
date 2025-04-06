from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, INT, DECIMAL, func


class BaseModel(DeclarativeBase):
    resource_id = Column(UUID, primary_key=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class WalletInfo(BaseModel):

    __tablename__ = "wallet_info"

    wallet_address = Column(String(50), nullable=False)
    balance = Column(DECIMAL(50, 2), nullable=False)
    bandwidth = Column(INT, nullable=False)
    energy = Column(INT, nullable=False)

    def __repr__(self) -> str:
        return f"WalletInfo({self.resource_id=}, {self.wallet_address=}, {self.balance=}, {self.bandwidth=}, {self.energy=})"
