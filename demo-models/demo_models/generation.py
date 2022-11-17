import os
import click

from demo_models.content import ContentFactory


@click.command()
@click.argument("n", type=int, help="number of object to generate")
@click.argument(
    "dest", type=click.Path(exists=True, dir_okay=True,
    file_okay=False), help="directory path for the data generation"
)
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
