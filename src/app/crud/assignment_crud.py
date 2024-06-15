from ._base_crud import CRUDBase
from ..models.assignment_model import Assignment
from sqlalchemy.orm import Session

class CRUDAssignment(CRUDBase[Assignment]):
    def read_by_course_id(self, course_id: int, db: Session) -> Assignment:
        asms = db.query(Assignment).filter(Assignment.course_id == course_id).all()
        return [a.__dict__ for a in asms]