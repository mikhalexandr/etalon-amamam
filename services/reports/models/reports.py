from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.postgres.initialization import Base


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object_id: Mapped[str] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"))
    photo_amount: Mapped[int] = mapped_column(nullable=False)
    known_amount: Mapped[int] = mapped_column(nullable=False)
    types_amount: Mapped[int] = mapped_column(nullable=False)
    workers_amount: Mapped[int] = mapped_column(nullable=False)
    good_workers_amount: Mapped[int] = mapped_column(nullable=False)
    bad_workers_amount: Mapped[int] = mapped_column(nullable=False)
    workers_violation_amount: Mapped[int] = mapped_column(nullable=False)
    object_violation_amount: Mapped[int] = mapped_column(nullable=False)
    is_safe: Mapped[int] = mapped_column(nullable=False)

    object_ = relationship(
        "ObjectModel",
        back_populates="reports"
    )
