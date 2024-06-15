from sqlalchemy import Column, String
from supertokens_backend.database.db_source import Base

class EmailPasswordUser(Base):
    __tablename__ = 'emailpassword_users'
    user_id = Column(String, primary_key=True)
    email = Column(String)

class ThirdPartyUser(Base):
    __tablename__ = 'thirdparty_users'
    user_id = Column(String, primary_key=True)
    email = Column(String)