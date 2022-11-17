from datetime import datetime
from pydantic import BaseModel
from pydantic_factories import ModelFactory

from .data import Data


class Content(BaseModel):
    date: datetime
    service: str
    payload: Data


class ContentFactory(ModelFactory[Content]):
    __model__ = Content
