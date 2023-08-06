import click
import yaml

from uservice.importer import import_from_string


@click.command()
@click.argument("service")
def schema(
        service: str,
):
    loaded_service = import_from_string(service)
    schema = loaded_service.schema()
    with open('asyncapi.yaml', 'w') as f:
        yaml.dump(schema, f)
