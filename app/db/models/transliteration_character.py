import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .common import Base


class TransliterationCharacter(Base):
    __tablename__ = "transliteration_characters"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    value = Column(String, nullable=False)
    character_id = Column(UUID(as_uuid=True),ForeignKey("characters.id", ondelete="CASCADE"),nullable=False)
    transliteration_system_id = Column(
        UUID(as_uuid=True), ForeignKey("transliteration_systems.id", ondelete="CASCADE"), nullable=False,
    )

    date_created = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    date_modified = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    character = relationship("Character", back_populates="transliteration_character")
    transliteration_system = relationship("TransliterationSystem",back_populates="transliteration_character")

    __table_args__ = (
        UniqueConstraint(
            "character_id",
            "transliteration_system_id",
            name="uq_transliteration_characters_character_id_system_id",
        ),
    )

    def __str__(self):
        return self.value
