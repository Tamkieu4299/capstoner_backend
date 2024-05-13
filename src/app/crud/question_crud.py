from ._base_crud import CRUDBase
from ..models.question_model import Question

class CRUDQuestion(CRUDBase[Question]):
    ...