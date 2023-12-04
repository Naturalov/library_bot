import pydantic


class SchemaBase(pydantic.BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True
