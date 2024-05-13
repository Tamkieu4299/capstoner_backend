from typing import List

from app.crud.job_crud import CRUDJob
from app.crud.job_item_crud import CRUDJobItem
from app.db.database import get_db
from app.models.job_model import Job
from app.models.job_item_model import JobItem
from app.utils.exception import CommonInvalid, NotFoundException
from app.utils.logger import setup_logger
from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from app.schemas.job_schema import JobRegisterSchema, JobResponseSchema, JobPictureUrlSchema, JobUpdateInfoSchema
from sqlalchemy.orm import Session
from ..secret import get_current_active_user
from ..utils import s3_driver
logger = setup_logger(__name__)

router = APIRouter()

job_crud = CRUDJob(Job)
job_item_crud = CRUDJobItem(JobItem)

@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def register_Job(
    job_data: JobRegisterSchema = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    if not current_user["user"].vendor_id:
        raise CommonInvalid(detail="User must own a vendor before create jobs.")
    url = s3_driver.upload(file = file, dest_dir = "avatar", protocol="")
    job_data_dict = job_data.dict()
    job_data_dict["created_by"] = current_user["user"].id
    job_data_dict["updated_by"] = current_user["user"].id
    job_data_dict["vendor_id"] = current_user["user"].vendor_id
    job_data_dict["picture"] = url
    new_Job = await job_crud.create(job_data_dict, db)
    if new_Job is None:
        logger.info(
            f"Fail to create job"
        )
        raise CommonInvalid(detail=f"Fail to create job")
    return new_Job.__dict__

@router.get(
    "/get-picture",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
)
async def get_picture(
    payload: JobPictureUrlSchema,
    current_user=Depends(get_current_active_user),
):
    presigned_url = s3_driver.generate_presigned_url("get_object", "wedi-image", payload.url)
    if presigned_url is None:
        logger.info(
            f"Fail to get url"
        )
        raise CommonInvalid(detail=f"Fail to get url")
    return presigned_url

@router.post("/update-job-info/{job_id}", response_model=JobResponseSchema)
def api_update_job_info(
    job_id: str,
    job_info: JobUpdateInfoSchema = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    job_info_dict = job_info.dict()
    if file:
        url = s3_driver.upload(file = file, dest_dir = "avatar", protocol="")
        job_info_dict["picture"] = url
    job = job_crud.update(
        job_id,
        job_info_dict,
        db,
    )

    if job is None:
        logger.info(f"Invalid Job with ID: {job_id}")
        raise NotFoundException(detail=f"Invalid Job with ID: {job_id}")

    return job.__dict__

@router.get("/search", response_model=List[JobResponseSchema])
async def search_jobs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    jobs = job_crud.get_all(db, skip, limit)
    jobs_dict_list = []
    for job in jobs:
        items = job_item_crud.get_items_by_job(job.id, db)
        job_dict = job.__dict__
        job_dict["items"] = items
        job_dict["vendor"] = job.vendor.__dict__
        jobs_dict_list.append(job_dict)
        
    logger.info(f"Number of jobs: {len(jobs)}")
    return jobs_dict_list


@router.get("/search/{vendor_id}", response_model=List[JobResponseSchema])
async def search_jobs_by_vendor(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    vendor_id: int = 0,
    current_user=Depends(get_current_active_user),
):
    jobs = job_crud.get_jobs_by_vendor(vendor_id, db, skip, limit)
    jobs_dict_list = []
    for job in jobs:
        items = job_item_crud.get_items_by_job(job.id, db)
        job_dict = job.__dict__
        job_dict["items"] = items
        job_dict["vendor"] = job.vendor.__dict__
        jobs_dict_list.append(job_dict)
        
    logger.info(f"Number of jobs: {len(jobs)}")
    return jobs_dict_list