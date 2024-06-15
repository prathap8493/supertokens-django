from sqlalchemy import Column, Integer,String,DateTime,func
from supertokens_backend.database.db_source import Base
from datetime import datetime

class SaveUserText(Base):
    __tablename__ = 'save_user_text'
    id = Column(Integer, primary_key=True)  # Auto-incrementing primary key
    user_uuid = Column(String, index=True, nullable=False)  # Not the primary key, but indexed for performance
    text = Column(String)
    created_by = Column(String(256), nullable=False)
    created_date = Column(DateTime, nullable=False, default=func.now())
    last_updated_by = Column(String(256), nullable=False)
    last_updated_date = Column(DateTime, nullable=False, default=func.now())