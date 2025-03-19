from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.postgres.initialization import Base


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object_id: Mapped[str] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"))
    date: Mapped[datetime] = mapped_column(nullable=False)
    completeness: Mapped[int] = mapped_column(nullable=False)
    is_safe: Mapped[bool] = mapped_column(nullable=False)

    object_ = relationship(
        "ObjectModel",
        back_populates="reports"
    )
