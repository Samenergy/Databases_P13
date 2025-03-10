from sqlalchemy.orm import Session
from models.credit_history import CreditHistory

def get_all_credit_histories(db: Session):
    return db.query(CreditHistory).all()

def create_credit_history(db: Session, credit_data):
    credit_history = CreditHistory(**credit_data)
    db.add(credit_history)
    db.commit()
    db.refresh(credit_history)
    return credit_history
