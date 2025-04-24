from sqlalchemy import Time, Date, ForeignKey, BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing_extensions import TypeVar

from services.database.engine import Base


class Device(Base):
    __tablename__ = 'devices'
    device_id: Mapped[int] = mapped_column(unique=True)


ModelType = TypeVar("ModelType", bound=Base)
