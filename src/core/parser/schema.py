import datetime

from pydantic import BaseModel, field_validator

from src.core.db.model import Bulletin


class BulletinSchema(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    delivery_basis_name: str
    volume: int
    total: int
    count: int
    date: datetime.date

    @field_validator("volume", mode='before')
    @classmethod
    def validate_volume(cls, value: str) -> int:
        return int(value) if value != "-" and value != "" else 0

    @field_validator("total", mode='before')
    @classmethod
    def validate_total(cls, value: str) -> int:
        return int(value) if value != "-" and value != "" else 0

    @field_validator("count", mode='before')
    @classmethod
    def validate_count(cls, value: str) -> int:
        return int(value) if value != "-" and value != "" else 0

    def to_model(self) -> Bulletin:
        return Bulletin(
            exchange_product_id=self.exchange_product_id,
            exchange_product_name=self.exchange_product_name,
            oil_id=self.exchange_product_id[:4],
            delivery_basis_id=self.exchange_product_id[4:7],
            delivery_basis_name=self.delivery_basis_name,
            delivery_type_id=self.exchange_product_id[-1],
            volume=self.volume,
            total=self.total,
            count=self.count,
            date=self.date,
        )
