from typing import List

from app.crud.vendor_crud import CRUDVendor
from app.crud.user_crud import CRUDUser
from app.db.database import get_db
from app.models.vendor_model import Vendor
from app.models.user_model import User
from app.utils.exception import CommonInvalid
from app.utils.logger import setup_logger
from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.vendor_schema import VendorRegisterSchema, VendorResponseSchema
from sqlalchemy.orm import Session
from ..secret import get_current_active_user

logger = setup_logger(__name__)

router = APIRouter()

vendor_crud = CRUDVendor(Vendor)
user_curd = CRUDUser(User)

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=VendorResponseSchema,
)
async def register_vendor(
    vendor_data: VendorRegisterSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    if current_user["user"].vendor_id:
        raise CommonInvalid(detail="User can only own 1 vendor.")

    business_license = vendor_data.business_license
    exist_vendor = vendor_crud.search_vendor_by_business_license(business_license, db)

    if exist_vendor:
        raise HTTPException(
            status_code=422, detail="This business license has been registered."
        )

    vendor_data_dict = vendor_data.dict()
    vendor_data_dict["created_by"] = current_user["user"].id
    vendor_data_dict["updated_by"] = current_user["user"].id
    new_vendor = await vendor_crud.create(vendor_data_dict,current_user["user"].id, db)
    if new_vendor is None:
        logger.info(
            f"Fail to create vendor"
        )
        raise CommonInvalid(detail=f"Fail to create vendor")
    return new_vendor.__dict__


@router.get("/search/", response_model=List[VendorResponseSchema])
async def get_vendors(
    db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    vendors = vendor_crud.get_all(db)
    vendors_dict_list = [i.__dict__ for i in vendors]
    logger.info(f"Number of vendors: {len(vendors)}")
    return vendors_dict_list
