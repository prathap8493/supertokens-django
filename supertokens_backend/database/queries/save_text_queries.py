from supertokens_backend.database.db_source import SessionLocal
from supertokens_backend.database.models.save_text import SaveUserText
from sqlalchemy import or_,func
from datetime import datetime,timedelta

class SaveUserTextQueries:

    @staticmethod
    def insert_text(user_id,text):
        session = SessionLocal()
        try:
            document = SaveUserText(
                user_uuid=user_id,
                text=text,
                created_by="system",
                created_date=datetime.utcnow(),
                last_updated_by="system",
                last_updated_date=datetime.utcnow(),
            )
            session.add(document)
            session.commit()
            return True
        
        except Exception as e:
            print(f"Error while creating the document: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def get_saved_texts(user_uuid):
        session = SessionLocal()
        try:
            session.begin()  # Explicitly begin a transaction
            records = session.query(SaveUserText).filter(SaveUserText.user_uuid == user_uuid).all()
            session.commit()  # Commit to make sure any locking or session-level caching is cleared
            
            if records:
                today = datetime.utcnow().date()
                one_week_ago = today - timedelta(days=7)

                result = [{'text': rec.text, 'created_date': rec.created_date.isoformat()} for rec in records]
                count_today = session.query(SaveUserText).filter(
                    SaveUserText.user_uuid == user_uuid,
                    func.date(SaveUserText.created_date) == today
                ).count()

                count_week = session.query(SaveUserText).filter(
                    SaveUserText.user_uuid == user_uuid,
                    SaveUserText.created_date >= one_week_ago
                ).count()

                return True, result, count_today, count_week

        except Exception as e:
            session.rollback()  # Rollback in case of exception
            return False, [], 0, 0
        finally:
            session.close()  # Ensure session is closed
