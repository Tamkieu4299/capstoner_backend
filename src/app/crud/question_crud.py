from ._base_crud import CRUDBase
from ..models.question_model import Question
from ..models.assignment_question_model import AssignmentQuestion
from sqlalchemy.orm import Session

class CRUDQuestion(CRUDBase[Question]):
    async def create(self, obj_in: dict, db: Session) -> Question:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.flush() 
        obj_assignment_question = AssignmentQuestion(**{"assignment_id": db_obj.assignment_id, "question_id": db_obj.id})
        db.add(obj_assignment_question)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def read_by_title(self, assignment_id: int, question_title: str, db: Session) -> Question:
        return db.query(Question).where(Question.assignment_id == assignment_id, Question.question_title == question_title).first()
    
    def read_by_assignment_id(self, assignment_id: int, db: Session) -> Question:
        return db.query(Question).filter(Question.assignment_id == assignment_id).all()