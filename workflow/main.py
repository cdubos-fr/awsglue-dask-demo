import dask.dataframe as df
import dask.bag as db
import dask
import numpy as np
from dask.distributed import Client
import click


@click.command()
@click.argument("path")
def read_json(path):
    print('read json')
    json_df = df.read_json(path, meta={'date': np.dtype('datetime64[ns]'), 'service': str, 'payload': object})
    print('map payload')
    data_df = delayed_sequence(json_df.payload).to_dataframe(meta={'age': int, 'name': str, 'contact_info': object})[['age', 'name', 'contact_info']]
    print('map contact info')
    contact_info = delayed_sequence(data_df.contact_info).to_dataframe(meta={'num_tel': str, 'email': str})[['num_tel', 'email']]
    print('join')
    print(json_df[['date', 'service']].join([data_df[['age', 'name']].compute() , contact_info.compute()]).compute())


if __name__ == '__main__':
    client = Client()
    delayed_sequence = dask.delayed(db.from_sequence)
    read_json()
