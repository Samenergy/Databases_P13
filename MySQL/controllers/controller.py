from sqlalchemy.orm import Session
from models.person import Person
from models.loan import Loan
from models.loan_financials import LoanFinancials
from models.credit_history import CreditHistory

def get_all_persons(db: Session):
    return db.query(Person).all()

def create_person(db: Session, person_data):
    person = Person(**person_data)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person

def create_person_with_details(db: Session, data):
    person = Person(
        age=data['person_age'],
        gender=data['person_gender'],
        education=data['person_education'],
        income=data['person_income'],
        emp_exp=data['person_emp_exp'],
        home_ownership=data['person_home_ownership']
    )
    db.add(person)
    db.commit()
    db.refresh(person)

    loan = Loan(
        person_id=person.id,
        loan_amount=data['loan_amnt'],
        loan_intent=data['loan_intent'],
        loan_status=data['loan_status']
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)

    loan_financials = LoanFinancials(
        loan_id=loan.id,
        interest_rate=data['loan_int_rate'],
        percent_income=data['loan_percent_income']
    )
    db.add(loan_financials)
    db.commit()
    db.refresh(loan_financials)

    credit_history = CreditHistory(
        person_id=person.id,
        credit_score=data['credit_score'],
        cred_hist_length=data['cb_person_cred_hist_length'],
        previous_defaults=data['previous_loan_defaults_on_file']
    )
    db.add(credit_history)
    db.commit()
    db.refresh(credit_history)

    return {
        "person": person,
        "loan": loan,
        "loan_financials": loan_financials,
        "credit_history": credit_history
    }

def get_person_by_id(db: Session, person_id: int):
    return db.query(Person).filter(Person.id == person_id).first()

def update_person(db: Session, person_id: int, update_data: dict):
    person = get_person_by_id(db, person_id)
    if person:
        for key, value in update_data.items():
            setattr(person, key, value)
        db.commit()
        db.refresh(person)
    return person

def patch_person(db: Session, person_id: int, patch_data: dict):
    return update_person(db, person_id, patch_data)
