from datetime import datetime
from typing import List, Optional

from wanted_models.base_model import BaseModel
from wanted_models.document import Document
from wanted_models.photo import Photo


class Record(BaseModel):
    platform_id: str
    url: Optional[str]
    fullname: List[str]
    alias: Optional[str]
    birth_date: str
    age: Optional[str]
    birth_place: Optional[str]
    addresses: Optional[List[str]]
    gender: Optional[str]
    nationality: Optional[str]
    citizenship: Optional[List[str]]
    identification: Optional[str]
    wanted_by: Optional[str]
    wanted_type: Optional[str]
    department: Optional[str]
    crime: Optional[List[str]]
    height: Optional[str]
    eye_colour: Optional[str]
    hair_color: Optional[str]
    weight: Optional[str]
    identifiers: Optional[List[str]]
    ethnic_origin: Optional[str]
    languages: Optional[List[str]]
    state_case: Optional[str]
    article: Optional[str]
    prevent_measure: Optional[str]
    resident: Optional[str]
    documents: Optional[Document]
    description: Optional[List[str]]
    publish_date: Optional[datetime]
    photo: Optional[Photo]
    criminal_record: Optional[str]
    remuneration: Optional[str]
