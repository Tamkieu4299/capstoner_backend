from ._base_crud import CRUDBase
from ..models.job_model import Job
from ..models.job_item_model import JobItem
from sqlalchemy.orm import Session

class CRUDJob(CRUDBase[Job]):
    async def create(self, obj_in: dict, db: Session) -> Job:
        obj_in_Job = {k: obj_in[k] for k in set(list(obj_in.keys())) - set(["items"])}
        db_job = self.model(**obj_in_Job)
        db.add(db_job)
        db.flush() 
        item_ids = obj_in["items"]
        obj_job_items = [JobItem(**{"job_id": db_job.id, "item_id": item_id}) for item_id in item_ids]
        db.add_all(obj_job_items)
        db.commit()
        db.refresh(db_job)
        return db_job
   
    def update(self, id: int, obj_in: dict, db: Session):
        if "items" in obj_in and len(obj_in["items"]):
            self.update_items(id, obj_in["items"], db)
        obj_in_Job = {k: obj_in[k] for k in set(list(obj_in.keys())) - set(["quantity"])}
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        for key, value in obj_in_Job.items():
            if not value:
                continue
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_items(self, id: int, new_items: list, db: Session):
        current_items = db.query(JobItem).filter(JobItem.job_id == id)
        current_items_item_id = [item.item_id for item in current_items]
        # Delete items
        delete_items = [item for item in current_items_item_id if item not in new_items]
        db.query(JobItem).filter(JobItem.item_id.in_(delete_items)).delete(synchronize_session=False)

        # Add items
        add_items = [item for item in new_items if item not in current_items_item_id]
        obj_job_items = [JobItem(**{"job_id": id, "item_id": item_id}) for item_id in add_items]
        db.add_all(obj_job_items)

    def get_jobs_by_vendor(self, vendor_id: int, db: Session, skip: int = 0, limit: int = 10):
        return db.query(Job).filter(Job.vendor_id == vendor_id).offset(skip).limit(limit).all()
        