from ._base_crud import CRUDBase
from ..models.item_model import Item

class CRUDItem(CRUDBase[Item]):
    ...