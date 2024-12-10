from sqlalchemy.ext.declarative import declarative_base

from .User import User
from .Contact import Contact
from .BasicInfo import BasicInfo
from .Location import Location
from .Area import Area
from .base import Base  # 導出 Base 供其他代碼使用

# 導出所有類別
__all__ = [ "User", "Contact", "BasicInfo", "Location", "Area", "Base"]

