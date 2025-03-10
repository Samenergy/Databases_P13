from sqlalchemy.orm import Session
from models.person import Person
from models.loan import Loan
from models.loan_financials import LoanFinancials
from models.credit_history import CreditHistory
from models.schemas import PersonCreate, LoanCreate, LoanFinancialsCreate, CreditHistoryCreate, PersonWithLoanResponse
from fastapi import HTTPException

# Create a person with associated loan, loan financials, and credit history
def create_person_with_loan_and_credit(
    db: Session, person_data: PersonCreate, loan_data: LoanCreate, loan_financial_data: LoanFinancialsCreate, credit_history_data: CreditHistoryCreate
):
    # Create the person
    person = Person(
        age=person_data.age,
        gender=person_data.gender,
        education=person_data.education,
        income=person_data.income,
        emp_exp=person_data.emp_exp,
        home_ownership=person_data.home_ownership
    )
    db.add(person)
    db.commit()
    db.refresh(person)

    # Create the loan
    loan = Loan(
        person_id=person.id,
        loan_amount=loan_data.loan_amount,
        loan_intent=loan_data.loan_intent,
        loan_status=loan_data.loan_status
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)

    # Create the loan financials
    loan_financial = LoanFinancials(
        loan_id=loan.id,
        interest_rate=loan_financial_data.interest_rate,
        percent_income=loan_financial_data.percent_income
    )
    db.add(loan_financial)
    db.commit()
    db.refresh(loan_financial)

    # Create credit history
    credit_history = CreditHistory(
        person_id=person.id,
        credit_score=credit_history_data.credit_score,
        cred_hist_length=credit_history_data.cred_hist_length,
        previous_defaults=credit_history_data.previous_defaults
    )
    db.add(credit_history)
    db.commit()
    db.refresh(credit_history)

    return {
        "person_age": person.age,
        "person_gender": person.gender,
        "person_education": person.education,
        "person_income": person.income,
        "person_emp_exp": person.emp_exp,
        "person_home_ownership": person.home_ownership,
        "loan_amnt": loan.loan_amount,
        "loan_intent": loan.loan_intent,
        "loan_int_rate": loan_financial.interest_rate,
        "loan_percent_income": loan_financial.percent_income,
        "cb_person_cred_hist_length": credit_history.cred_hist_length,
        "credit_score": credit_history.credit_score,
        "previous_loan_defaults_on_file": credit_history.previous_defaults,
        "loan_status": loan.loan_status
    }

# Get all persons with associated data
def get_all_persons_with_data(db: Session):
    persons = db.query(Person).all()
    result = []
    for person in persons:
        loan = db.query(Loan).filter(Loan.person_id == person.id).first()
        loan_financial = db.query(LoanFinancials).filter(LoanFinancials.loan_id == loan.id).first()
        credit_history = db.query(CreditHistory).filter(CreditHistory.person_id == person.id).first()
        result.append({
            "person_age": person.age,
            "person_gender": person.gender,
            "person_education": person.education,
            "person_income": person.income,
            "person_emp_exp": person.emp_exp,
            "person_home_ownership": person.home_ownership,
            "loan_amnt": loan.loan_amount,
            "loan_intent": loan.loan_intent,
            "loan_int_rate": loan_financial.interest_rate,
            "loan_percent_income": loan_financial.percent_income,
            "cb_person_cred_hist_length": credit_history.cred_hist_length,
            "credit_score": credit_history.credit_score,
            "previous_loan_defaults_on_file": credit_history.previous_defaults,
            "loan_status": loan.loan_status
        })
    return result

# Get a person by ID with associated data
def get_person_by_id(db: Session, person_id: int):
    person = db.query(Person).filter(Person.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    
    loan = db.query(Loan).filter(Loan.person_id == person.id).first()
    loan_financial = db.query(LoanFinancials).filter(LoanFinancials.loan_id == loan.id).first()
    credit_history = db.query(CreditHistory).filter(CreditHistory.person_id == person.id).first()
    
    return {
        "person_age": person.age,
        "person_gender": person.gender,
        "person_education": person.education,
        "person_income": person.income,
        "person_emp_exp": person.emp_exp,
        "person_home_ownership": person.home_ownership,
        "loan_amnt": loan.loan_amount,
        "loan_intent": loan.loan_intent,
        "loan_int_rate": loan_financial.interest_rate,
        "loan_percent_income": loan_financial.percent_income,
        "cb_person_cred_hist_length": credit_history.cred_hist_length,
        "credit_score": credit_history.credit_score,
        "previous_loan_defaults_on_file": credit_history.previous_defaults,
        "loan_status": loan.loan_status
    }
