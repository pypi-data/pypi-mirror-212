from typing import List

from wanted_models.base_model import BaseModel


class Photo(BaseModel):
    url: List[str]
