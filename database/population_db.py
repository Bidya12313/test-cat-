from database.engine import Base, db_engine
from .models import Cat, Mission, Target


tables = [Cat.__table__, Mission.__table__, Target.__table__]


def create_tables():
    Base.metadata.create_all(db_engine, tables=tables)


if __name__ == "__main__":
    create_tables()
