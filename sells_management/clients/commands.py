import click
from clients.models import Client
from clients.services import ClientService


@click.group()  # This makes "clients()" a group
def clients():
    """
    Manages the clients lifecycle.
    """
    pass


@clients.command()
@click.option('-n', '--name',
              type=str,
              prompt=True,
              help='The client name.')
@click.option('-c', '--company',
              type=str,
              prompt=True,
              help='The client company.')
@click.option('-e', '--email',
              type=str,
              prompt=True,
              help='The client email.')
@click.option('-p', '--position',
              type=str,
              prompt=True,
              help='The client position.')
@click.pass_context
def create(ctx, name, company, email, position):
    """
    Create a new client.
    """
    click.echo(f'Creating client {name}...')
    client = Client(name, company, email, position)
    client_service = ClientService(ctx.obj['clients_table'])

    client_service.create_client(client)


@clients.command()
@click.pass_context
def list(ctx):
    """
    List all clients.
    """
    click.echo('Listing clients...')
    client_service = ClientService(ctx.obj['clients_table'])
    clients = client_service.list_clients()
    click.echo('-' * 131)
    click.echo('| {:<40} | {:>10} | {:>15} | {:>25} | {:>25} |'.format(
        'ID', 'NAME', 'COMPANY', 'EMAIL', 'POSITION'))
    click.echo('-' * 131)
    for client in clients:
        click.echo('| {:<40} | {:>10} | {:>15} | {:>25} | {:>25} |'.format(
            client['uid'], client['name'], client['company'], client['email'], client['position']))
    click.echo('-' * 131)


@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def update(ctx, client_uid):
    """
    Update a client.
    """
    click.echo(f'Updating client {client_uid}...')
    client_service = ClientService(ctx.obj['clients_table'])
    clients = client_service.list_clients()
    filtered_list = [
        client for client in clients if client['uid'] == client_uid]
    if len(filtered_list) > 0:
        client = filtered_list[0]
        client = _update_client_flow(Client(**client))
        client_service.update_client(client)
        click.echo(f'Client {client_uid} updated!')
    else:
        click.echo('Client not found.')


@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def delete(ctx, client_uid):
    """
    Delete a client.
    """
    click.echo(f'Deleting client {client_uid}...')
    client_service = ClientService(ctx.obj['clients_table'])
    clients = client_service.list_clients()
    filtered_list = [
        client for client in clients if client['uid'] == client_uid]
    if len(filtered_list) > 0:
        client = filtered_list[0]
        client_service.delete_client(Client(**client))
        click.echo(f'Client {client_uid} deleted!')
    else:
        click.echo('Client not found.')


def _update_client_flow(client):
    click.echo('Leave the prompts empty if you do not want to modify the value')
    client.name = click.prompt(
        'New name', type=str, default=client.name)
    client.company = click.prompt(
        'New company', type=str, default=client.company)
    client.email = click.prompt(
        'New email', type=str, default=client.email)
    client.position = click.prompt(
        'New position', type=str, default=client.position)

    return client


all = clients
