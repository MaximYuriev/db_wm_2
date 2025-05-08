from datetime import datetime, date

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        onupdate=func.now(),
    )


class Bulletin(Base):
    __tablename__ = "spimex_trading_results"
    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[date]

    @classmethod
    def from_df_row(cls, row: dict[str, str]) -> "Bulletin":
        return cls(
            exchange_product_id=row["exchange_product_id"],
            exchange_product_name=row["exchange_product_name"],
            oil_id=row["exchange_product_id"][:4],
            delivery_basis_id=row["exchange_product_id"][4:7],
            delivery_basis_name=row["delivery_basis_name"],
            delivery_type_id=row["exchange_product_id"][-1],
            volume=int(row["volume"]),
            total=int(row["total"]),
            count=int(row["count"]),
            date=row["date"],
        )
