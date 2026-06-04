import random
import uuid
from typing import Generic, TypeVar

from app.db.models.alphabet import Alphabet, WrittingDirection, WrittingSystem
from app.db.models.script_family import ScriptFamily
from app.db.models.character import  AlphabetUnitType, Character
from app.db.models.transliteration_character import TransliterationCharacter
from app.db.models.transliteration_system import TransliterationSystem
import factory
import factory.fuzzy
import sqlalchemy as sa

from sqlalchemy import func, select

from app.db.session import test_session
from app.config import get_settings

global_settings = get_settings()
T = TypeVar('T')


class BaseMetaFactory(Generic[T], factory.base.FactoryMetaClass):
    def __call__(cls, *args, **kwargs) -> T:
        return super().__call__(*args, **kwargs)


class BaseSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = test_session
        sqlalchemy_session_persistence = "flush"

    @classmethod
    def _save(cls, model_class, session, args, kwargs):
        # Add user context for audit trigger
        # Object is created, but not flushed yet
        obj = model_class(*args, **kwargs)

        session.add(obj)
        session.flush([obj])
        return obj


class SciptFamilyFactory(BaseSQLAlchemyModelFactory, metaclass=BaseMetaFactory[ScriptFamily]):
    class Meta:
        model = ScriptFamily

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")


class AlphabetFactory(BaseSQLAlchemyModelFactory, metaclass=BaseMetaFactory[Alphabet]):
    class Meta:
        model = Alphabet

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    writting_system = factory.fuzzy.FuzzyChoice([
        WrittingSystem.ALPHABET,
        WrittingSystem.ABJAD,
        WrittingSystem.ABUGIDA,
        WrittingSystem.SYLLABARY,
        WrittingSystem.LOGOGRAPHIC,
        WrittingSystem.MIXED,
    ])
    writting_direction = factory.fuzzy.FuzzyChoice([
        WrittingDirection.LTR,
        WrittingDirection.RTL,
        WrittingDirection.TTB,
    ])
    script_family = factory.SubFactory(SciptFamilyFactory)


class CharacterFactory(BaseSQLAlchemyModelFactory, metaclass=BaseMetaFactory[Character]):
    class Meta:
        model = Character

    id = factory.LazyFunction(uuid.uuid4)
    value = factory.Sequence(lambda n: f"char_{n}")
    name = factory.Faker("word")
    unit_type = factory.fuzzy.FuzzyChoice([
        AlphabetUnitType.LETTER,
        AlphabetUnitType.SEQUENCE,
        AlphabetUnitType.PUNCTUATION,
    ])
    unicode_codepoint = None
    alphabet = factory.SubFactory(AlphabetFactory)


class TransliterationSystemFactory(BaseSQLAlchemyModelFactory, metaclass=BaseMetaFactory[TransliterationSystem]):
    class Meta:
        model = TransliterationSystem

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("sentence")


class TransliterationCharacterFactory(BaseSQLAlchemyModelFactory, metaclass=BaseMetaFactory[TransliterationCharacter]):
    class Meta:
        model = TransliterationCharacter

    id = factory.LazyFunction(uuid.uuid4)
    value = factory.Sequence(lambda n: f"trans_char_{n}")
    character = factory.SubFactory(CharacterFactory)
    transliteration_system = factory.SubFactory(TransliterationSystemFactory)
