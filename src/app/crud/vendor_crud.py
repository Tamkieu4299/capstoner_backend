from ._base_crud import CRUDBase
from ..models.vendor_model import Vendor
from ..models.user_model import User
from sqlalchemy.orm import Session


class CRUDVendor(CRUDBase[Vendor]):
    async def create(self, obj_in: dict, user_id: int, db: Session) -> Vendor:
        db_vendor = self.model(**obj_in)
        db.add(db_vendor)
        db.flush() 
        db_user = db.query(User).filter(User.id == user_id).first()
        setattr(db_user, "vendor_id", db_vendor.id)
        db.commit()
        db.refresh(db_vendor)
        return db_vendor

    
    def search_vendor_by_business_license(
        self, business_license: str, db: Session
    ) -> Vendor:
        vendor = (
            db.query(Vendor)
            .filter(
                Vendor.business_license == business_license
                and Vendor.is_deleted == False
            )
            .first()
        )
        return vendor
