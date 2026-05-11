from typing import Sequence
from sqlmodel import Session, select
from ..db.models.lockers import Lockers

class LockerRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all_lockers(self) -> Sequence[Lockers]:
        statement = select(Lockers)

        return self.session.exec(statement).all()

