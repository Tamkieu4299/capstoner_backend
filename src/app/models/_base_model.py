from .mixin_base_model import MixinBaseModel
from .naming_convention import convention
from sqlalchemy import MetaData, Column, DateTime, func, Boolean
from sqlalchemy.ext.declarative import as_declarative
from app.constants.config import Settings, get_settings


settings: Settings = get_settings()

_metadata_obj = MetaData(naming_convention=convention)

@as_declarative(metadata=_metadata_obj)
class BaseModel(MixinBaseModel):
    __abstract__ = True
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
