import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import (BigInteger, CheckConstraint, Column, DateTime, Enum,
                        ForeignKey, Index, String)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from .common import Base


class WrittingSystem(str, enum.Enum):
    ALPHABET = "alphabet"
    ABJAD = "abjad"
    ABUGIDA = "abugida"
    SYLLABARY = "syllabary"
    LOGOGRAPHIC = "logographic"
    MIXED = "mixed"


class WrittingDirection(str, enum.Enum):
    RTL = "rtl"
    LTR = "ltr"
    TTB = "ttb"



class Alphabet(Base):
    """ Alphabet table"""
    __tablename__ = "alphabets"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    writting_system = Column(Enum(WrittingSystem), nullable=False)
    writting_direction = Column(Enum(WrittingDirection), nullable=False)
    script_family_id = Column(
        UUID(as_uuid=True),
        ForeignKey("script_families.id", ondelete="RESTRICT"),
        nullable=False,
    )

    date_created = Column("date_created", DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    date_modified = Column("date_modified", DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    script_family = relationship("ScriptFamily", back_populates="alphabets")
    characters = relationship("Character", back_populates="alphabet")

    def __str__(self):
        return f"{self.name}"
