import os
from datetime import datetime
from pydantic import BaseModel
from pydantic_factories import ModelFactory
import dask.dataframe as df
import dask.bag as db
import dask
import numpy as np

from dask.distributed import Client


client = Client()


class Contact(BaseModel):
    num_tel: str
    email: str


class ContactFactory(ModelFactory[Contact]):
    __model__ = Contact


class Data(BaseModel):
    name: str
    age: int
    contact_info: Contact


class DataFactory(ModelFactory[Data]):
    __model__ = Data


class Content(BaseModel):
    date: datetime
    service: str
    payload: Data


class ContentFactory(ModelFactory[Content]):
    __model__ = Content



def generate(n: int, dest: str='write') -> list[str]:
    directory = os.path.join(os.path.dirname(__file__), dest)
    if os.path.isfile(directory):
        raise NotADirectoryError(f'{directory=} is a file')
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(n):
        filename = f'content-{i}.json'
        content = ContentFactory.build()
        with open(os.path.join(directory, filename), mode='w') as f:
            f.write(content.json())

delayed_sequence = dask.delayed(db.from_sequence)


def read_json(path):
    print('read json')
    json_df = df.read_json(path, meta={'date': np.dtype('datetime64[ns]'), 'service': str, 'payload': object})
    print('map payload')
    data_df = delayed_sequence(json_df.payload).to_dataframe(meta={'age': int, 'name': str, 'contact_info': object})[['age', 'name', 'contact_info']]
    print('map contact info')
    contact_info = delayed_sequence(data_df.contact_info).to_dataframe(meta={'num_tel': str, 'email': str})[['num_tel', 'email']]
    print('join')
    return json_df[['date', 'service']].join([data_df[['age', 'name']].compute() , contact_info.compute()])
