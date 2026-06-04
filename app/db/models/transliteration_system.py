import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .common import Base


class TransliterationSystem(Base):
    __tablename__ = "transliteration_systems"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    date_created = Column("date_created", DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    date_modified = Column("date_modified", DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    transliteration_character = relationship("TransliterationCharacter", back_populates="transliteration_system")

    def __str__(self):
        return self.name
