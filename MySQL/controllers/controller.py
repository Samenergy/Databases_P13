from sqlalchemy.orm import Session
from models.person import Person

def get_all_persons(db: Session):
    return db.query(Person).all()

def create_person(db: Session, person_data):
    person = Person(**person_data)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person
