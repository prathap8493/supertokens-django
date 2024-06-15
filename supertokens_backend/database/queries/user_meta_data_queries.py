from ..db_source import SessionLocal
from typing import Dict
from ..models.user_meta_data import UserMetaData
from datetime import datetime


class UserMetaDataQueries:

    @staticmethod
    def get_meta_data_details(user_id):
        session = SessionLocal()
        try:
            record = session.query(UserMetaData).filter_by(user_id = user_id).first()
            print(f"record:{record}")
            if record:
                return True
            return False
        except Exception as e:
            print(f"error:{str(e)}")
            session.rollback()
            return True
        finally:
            session.close()