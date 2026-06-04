import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .common import Base


class ScriptFamily(Base):
    __tablename__ = "script_families"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)

    date_created = Column("date_created", DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    date_modified = Column("date_modified", DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    alphabets = relationship("Alphabet", back_populates="script_family")
