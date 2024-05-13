
from app.crud.review_crud import CRUDReview
from app.db.database import get_db
from app.models.review_model import Review
from app.utils.exception import CommonInvalid
from app.utils.logger import setup_logger
from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from app.schemas.review_schema import ReviewRegisterSchema, ReviewResponseSchema, ReviewAttachmentSchema
from sqlalchemy.orm import Session
from ..utils import s3_driver

from ..secret import get_current_active_user
logger = setup_logger(__name__)

router = APIRouter()

review_crud = CRUDReview(Review)

@router.post(
"/add",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewResponseSchema,
)
async def register_review(
    review_data: ReviewRegisterSchema = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    review_data_dict = review_data.dict()
    if file:
        url = s3_driver.upload(file = file, dest_dir = "attachment", protocol="")
        review_data_dict["attachment"] = url
    review_data_dict["created_by"] = current_user["user"].id
    new_review = await review_crud.create(review_data_dict, db)
    if new_review is None:
        logger.info(
            f"Fail to create review"
        )
        raise CommonInvalid(detail=f"Fail to create review")
    return new_review.__dict__

@router.get(
    "/get-attachment",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
)
async def get_attachment(
    payload: ReviewAttachmentSchema,
    current_user=Depends(get_current_active_user),
):
    presigned_url = s3_driver.generate_presigned_url("get_object", "wedi-image", payload.url)
    if presigned_url is None:
        logger.info(
            f"Fail to get url"
        )
        raise CommonInvalid(detail=f"Fail to get url")
    return presigned_url