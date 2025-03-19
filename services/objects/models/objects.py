from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.postgres.initialization import Base


class ObjectModel(Base):
    __tablename__ = "objects"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    reports_count: Mapped[int] = mapped_column(default=0)

    reports = relationship(
        "ReportModel",
        back_populates="object_",
        cascade="all, delete-orphan"
    )
