from sqlalchemy.orm import Session
from models.loan import Loan

def get_all_loans(db: Session):
    return db.query(Loan).all()

def create_loan(db: Session, loan_data):
    loan = Loan(**loan_data)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan
