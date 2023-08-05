from sqlalchemy import create_engine

from .deployed_models import Base


def get_engine(db_path):
    return create_engine("sqlite:///{}".format(db_path))


def init_tables(engine):
    Base.metadata.create_all(engine)
