import os
import pathlib
import sys
# import random
# from uuid import UUID

from alembic import command
from alembic.config import Config
# from sqlalchemy import func, select
from sqlalchemy_utils import create_database, drop_database

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from app.factory.factories import BaseSQLAlchemyModelFactory, SciptFamilyFactory
from app.config import get_settings
from app.db.session import session


# Map main db session to factories
BaseSQLAlchemyModelFactory._meta.sqlalchemy_session = session
SciptFamilyFactory._meta.sqlalchemy_session = session


# DB setup
print("Setting up database")
if get_settings().ENVIRONMENT == "local":
    DB_URL = get_settings().POSTGRES_URL
else:
    DB_URL = os.getenv("DB_URL", "DB_URL")
drop_database(DB_URL)
create_database(DB_URL)
alembic_config_file = os.path.join(get_settings().ROOT_DIR, "..", "alembic.ini")
alembic_cfg = Config(alembic_config_file)
alembic_cfg.set_main_option("sqlalchemy.url", DB_URL)
command.upgrade(alembic_cfg, "head")


# Script Families
print("Creating Script Families")
workspace = SciptFamilyFactory(name="Test")

session.commit()
