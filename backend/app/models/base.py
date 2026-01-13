"""Base SQLAlchemy model with common fields."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class BaseModel(Base):
    """Abstract base model with common fields for all entities.

    Includes:
    - id: UUID primary key
    - created_at: Timestamp of creation
    - updated_at: Timestamp of last update
    - deleted_at: Soft delete timestamp (null if not deleted)
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        index=True,
    )

    @property
    def is_deleted(self) -> bool:
        """Check if the record has been soft deleted."""
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        """Mark the record as soft deleted."""
        self.deleted_at = datetime.now()
