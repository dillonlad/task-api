from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, nullable=False, default=2)  # Default to Medium priority
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    created = Column(DateTime, default=func.now(), nullable=False)  # pylint: disable=not-callable
