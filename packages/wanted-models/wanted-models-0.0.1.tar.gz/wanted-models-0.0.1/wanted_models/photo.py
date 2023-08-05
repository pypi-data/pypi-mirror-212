from typing import List

from pydantic import BaseModel


class Photo(BaseModel):
    url: List[str]
