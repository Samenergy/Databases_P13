from sqlalchemy.orm import Session
from models.loan_financials import LoanFinancials

def get_all_loan_financials(db: Session):
    return db.query(LoanFinancials).all()

def create_loan_financials(db: Session, financial_data):
    loan_financials = LoanFinancials(**financial_data)
    db.add(loan_financials)
    db.commit()
    db.refresh(loan_financials)
    return loan_financials
