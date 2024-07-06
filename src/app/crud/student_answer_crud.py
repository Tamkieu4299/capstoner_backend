from ._base_crud import CRUDBase
from ..models.student_answer_model import StudentAnswer
from sqlalchemy.orm import Session

class CRUDStudenAnswer(CRUDBase[StudentAnswer]):
    def read_by_assignment_id(self, assignment_id: int, db: Session):
        return db.query(StudentAnswer).filter(StudentAnswer.assignment_id == assignment_id).all()
    
    def read_by_assignment_id_sort_by_student_name(self, assignment_id: int, db: Session):
        return db.query(StudentAnswer).filter(StudentAnswer.assignment_id == assignment_id).order_by(StudentAnswer.student_name).all()