from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


from configs.Environment import get_environment_variables


env = get_environment_variables()
Engine = create_engine(env.DATABASE_URL, echo=env.DEBUG_MODE, future=True)


class Database:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.session = sessionmaker(autoflush=False, bind=Engine)
        return cls.instance


def get_db_connection():
    session = Database()
    db = scoped_session(session.session)
    try:
        yield db
    finally:
        db.close()
