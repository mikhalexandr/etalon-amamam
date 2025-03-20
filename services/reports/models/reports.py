from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.postgres.initialization import Base


# Модель отчета
class ReportModel(Base):
    __tablename__ = "reports"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column()
    object_id: Mapped[str] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"))
    photo_amount: Mapped[int] = mapped_column(nullable=False)
    known_amount: Mapped[int] = mapped_column(nullable=False)
    types_amount: Mapped[int] = mapped_column(nullable=False)
    workers_amount: Mapped[int] = mapped_column(nullable=False)
    workers_violation_amount: Mapped[int] = mapped_column(nullable=False)
    object_violation_amount: Mapped[int] = mapped_column(nullable=False)
    is_safe: Mapped[int] = mapped_column(nullable=False)

    object_ = relationship(
        "ObjectModel",
        back_populates="reports"
    )
