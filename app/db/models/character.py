import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .common import Base


class AlphabetUnitType(str, enum.Enum):
    LETTER = "letter"
    SEQUENCE = "sequence"
    PUNCTUATION = "punctuation"


class Character(Base):
    __tablename__ = "characters"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    alphabet_id = Column(UUID(as_uuid=True),ForeignKey("alphabets.id", ondelete="RESTRICT"),nullable=False)

    value = Column(String, nullable=False)
    name = Column(String, nullable=True)
    unit_type = Column(Enum(AlphabetUnitType), nullable=False)
    unicode_codepoint = Column(String, nullable=True)

    date_created = Column("date_created", DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    date_modified = Column("date_modified", DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    alphabet = relationship("Alphabet", back_populates="characters")
    transliteration_character = relationship("TransliterationCharacter", back_populates="character")

    __table_args__ = (
        UniqueConstraint("alphabet_id", "value", name="uq_characters_alphabet_id_value"),
    )

    def __str__(self):
        return f"{self.value}"
