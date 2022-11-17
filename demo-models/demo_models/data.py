from pydantic import BaseModel
from pydantic_factories import ModelFactory
from .contact import Contact


class Data(BaseModel):
    name: str
    age: int
    contact_info: Contact


class DataFactory(ModelFactory[Data]):
    __model__ = Data
