from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import TypeVar, Generic, List

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: ModelType):
        self.model = model

    async def create(self, obj_in: dict, db: Session):
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read(self, id: int, db: Session):
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, id: int, obj_in: dict, db: Session):
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        for key, value in obj_in.items():
            if not value:
                continue
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def soft_delete(self, id: int, db: Session):
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        db_obj.is_deleted = True
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, id: int, db: Session):
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        db.delete(db_obj)
        db.commit()
        return db_obj

    def get_all(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(self.model).offset(skip).limit(limit).all()

    async def bulk_create(self, objs_in: List[dict], db: Session):
        db_objs = [self.model(**obj_in) for obj_in in objs_in]
        db.add_all(db_objs)
        db.commit()
        for db_obj in db_objs:
            db.refresh(db_obj)
        return db_objs