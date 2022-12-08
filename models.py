from sqlalchemy import create_engine, Integer, String, Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///data.db?check_same_thread=False')


class Content(Base):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    channel_id = Column(Integer)
    content = Column(String)
    media_content = Column(String)
    created_at = Column(DateTime)
    edited_at = Column(DateTime, nullable=True)
    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)


Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session_db = Session()
