from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    db_url: str


class DBClient:
    def __init__(self):
        self._settings = DBSettings()
        self.engine = create_engine(self._settings.db_url)
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """
        Using yield is more efficient for FastAPI and will ensure db session is closed after request is complete.
        """

        db_session = self._session()
        try:
            yield db_session
        finally:
            db_session.close()
