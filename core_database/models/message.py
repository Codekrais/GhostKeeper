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
    from .user import User
class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="messages")
    text: Mapped[str] = mapped_column(nullable=True, default="", server_default="")
    type: Mapped[str] = mapped_column(nullable=True, default="", server_default="")
    file_id: Mapped[str] = mapped_column(nullable=True, default="", server_default="")

