from ..secret import get_current_active_user
from ..models.item_model import Item
from ..crud.item_crud import CRUDItem
from ..utils.logger import setup_logger
from app.db.database import get_db
from app.utils.exception import CommonInvalid
from ..schemas.item_schema import ItemRegisterSchema, ItemResponseSchema, ItemUpdateInfoSchema
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

logger = setup_logger(__name__)

router = APIRouter()

item_crud = CRUDItem(Item)

@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemRegisterSchema,
)
async def register_item(
    item_data: ItemRegisterSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    item_data_dict = item_data.dict()
    new_item = await item_crud.create(item_data_dict, db)
    if new_item is None:
        logger.info(
            f"Fail to create item"
        )
        raise CommonInvalid(detail=f"Fail to create item")
    return new_item.__dict__