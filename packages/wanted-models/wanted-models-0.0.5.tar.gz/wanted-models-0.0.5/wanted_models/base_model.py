from pydantic import BaseModel as PydanticBaseModel, validator


class BaseModel(PydanticBaseModel):

    @validator('*')
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and v.strip() == '':
            return None
        elif isinstance(v, list) and v[0] == '':
            return None
        return v

    @validator('*')
    def strip(cls, v):
        if isinstance(v, str):
            return v.strip()

        if isinstance(v, list):
            return [i.strip() if isinstance(i, str) else i for i in v]

        return v
