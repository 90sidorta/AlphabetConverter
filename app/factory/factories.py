import uuid
from typing import Generic, TypeVar

from app.db.models.script_family import ScriptFamily
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
    name = factory.Faker("company")
