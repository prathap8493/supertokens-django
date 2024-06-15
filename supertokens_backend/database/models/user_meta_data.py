from sqlalchemy import Column, String
from supertokens_backend.database.db_source import Base

class UserMetaData(Base):
    __tablename__ = 'user_metadata'
    user_id = Column(String, primary_key=True)