from ._base_crud import CRUDBase
from ..models.removed_word_model import RemovedWords
from sqlalchemy.orm import Session

class CRUDRemovedWord(CRUDBase[RemovedWords]):
    async def read_by_student_answer_id(self, student_answer_id: int, db: Session):
        return db.query(RemovedWords).filter(RemovedWords.student_answer_id == student_answer_id).all()