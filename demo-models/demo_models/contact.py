from pydantic import BaseModel
from pydantic_factories import ModelFactory



class Contact(BaseModel):
    num_tel: str
    email: str


class ContactFactory(ModelFactory[Contact]):
    __model__ = Contact
