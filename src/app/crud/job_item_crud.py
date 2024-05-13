from ._base_crud import CRUDBase
from ..models.job_item_model import JobItem
from sqlalchemy.orm import Session

class CRUDJobItem(CRUDBase[JobItem]):
    def get_items_by_job(self, job_id: int, db: Session):
        db_job_items = db.query(JobItem).filter(JobItem.job_id == job_id).all()
        return [ji.item.__dict__ for ji in db_job_items]