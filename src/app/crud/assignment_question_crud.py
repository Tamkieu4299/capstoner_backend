from ._base_crud import CRUDBase
from ..models.assignment_question_model import AssignmentQuestion
from sqlalchemy.orm import Session

class CRUDAssignmentQuestion(CRUDBase[AssignmentQuestion]):
    def get_questions_by_assignment(self, assignment_id: int, db: Session):
        db_obj = db.query(AssignmentQuestion).filter(AssignmentQuestion.assignment_id == assignment_id).all()
        return [o.question.__dict__ for o in db_obj]