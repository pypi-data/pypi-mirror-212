from datetime import datetime
from typing import Optional

from wanted_models.base_model import BaseModel


class Document(BaseModel):
    identification: Optional[str]
    type: Optional[str]
    serial_num: Optional[str]
    number: Optional[str]
    issue_date: Optional[datetime]
    expire_date: Optional[datetime]
