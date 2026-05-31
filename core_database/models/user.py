from typing import List, TYPE_CHECKING
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:
    from .message import Message

class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(nullable=True, default="", server_default="")
    fullname: Mapped[str] = mapped_column(nullable=True, default="", server_default="")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user")
