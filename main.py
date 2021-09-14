'''
Created Date: Sunday September 12th 2021 9:45:19 pm
Author: Andrés X. Vargas
-----
Last Modified: Monday September 13th 2021 1:54:38 am
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
import sys
import csv
import os

CLIENT_TABLE = '.clients.csv'
CLIENT_SCHEMA = ['name', 'company', 'email', 'position']
clients = []


def _initialize_clients_from_storage():
    global clients
    try:
        with open(CLIENT_TABLE, 'r') as f:
            reader = csv.DictReader(f, fieldnames=CLIENT_SCHEMA)
            for row in reader:
                clients.append(row)
    except IOError:
        print('File does not exist')


def _save_clients_to_storage():
    global clients
    tmp_table_name = f'{CLIENT_TABLE}.tmp'
    try:
        with open(tmp_table_name, 'w') as f:            
            writer = csv.DictWriter(f, fieldnames=CLIENT_SCHEMA)
            writer.writerows(clients)
        os.remove(CLIENT_TABLE)
        os.rename(tmp_table_name, CLIENT_TABLE)
    except IOError:
        print('File does not exist')


def create_client(client):
    id, client_found = search_client(client['name'])
    if(client_found):
        print('Client already exist')
    else:
        clients.append(client)
        print('Client added')


def update_client(client_id, new_client):
    global clients
    clients = list(map(lambda x: new_client if x[0] ==
                    int(client_id) else x[1], enumerate(clients)))
    print(clients)
    print('Client updated')


def delete_client(client_id):
    global clients
    clients = list(map(lambda x: x[1] if x[0] != int(client_id) else None , enumerate(clients)))
    clients = list(filter(lambda x: x != None, clients))
    print('Client deleted')


def search_client(client_name):
    global clients
    i = 0
    for client in clients:
        if client['name'] == client_name:
            return i, client
        i += 1
    return None, None


def list_clients():
    global clients
    print('List of clients: ')
    print('-' * 94)
    print('| {:<8} | {:>10} | {:>15} | {:>25} | {:>20} |'.format(
        'ID', 'NAME', 'COMPANY', 'EMAIL', 'POSITION'))
    print('-' * 94)
    for idx, client in enumerate(clients):
        print('| {:<8} | {:>10} | {:>15} | {:>25} | {:>20} |'.format(
            idx, client['name'], client['company'], client['email'], client['position']))
    print('-' * 94)


def _get_client_field(field_name):
    field = None
    while not field or field.isspace():
        field = input(f'What is the client {field_name}? ')
        if not field or field.isspace():
            print(f'Please enter a valid {field_name}')
        if field == 'exit':
            field = None
            break
    if field == None:
        _exit_program()

    return field


def _get_client():
    client = {
        'name': _get_client_field('name'),
        'company': _get_client_field('company'),
        'email': _get_client_field('email'),
        'position': _get_client_field('position')
    }
    return client


# def _get_client_name():
#     client_name = None
#     while not client_name or client_name.isspace():
#         client_name = input('What is the client name? ')
#         if client_name == 'exit':
#             client_name = None
#             break
#         if not client_name or client_name.isspace():
#             print('Please enter a client name')

    # if client_name == None:
    #     _exit_program()
    # return client_name


def _exit_program():
    print('Bye')
    sys.exit()


def _client_exists(client_id):
    print(client_id)
    return len(list(filter(lambda x: x[0] == int(client_id), enumerate(clients)))) > 0


def print_welcome():
    print('Welcome to the client management system')
    print('*' * 50)
    print('What would you like to do today?')
    print('[C]reate client')
    print('[U]pdate client')
    print('[D]elete client')
    print('[S]earch client')
    print('[L]ist clients')
    print('[E]xit')


def main():
    _initialize_clients_from_storage()
    print_welcome()
    command = input("Select an command: ")
    command = command.upper()

    if command == 'C':
        client = _get_client()
        create_client(client)

    elif command == 'U':
        client_id = _get_client_field('id')
        if (_client_exists(client_id)):
            update_client(client_id, _get_client())
        else:
            print('Client does not exist')

    elif command == 'D':
        client_id = _get_client_field('id')
        if (_client_exists(client_id)):
            delete_client(client_id)
        else:
            print('Client does not exist')

    elif command == 'S':
        client_name = _get_client_field('name')
        id, client = search_client(client_name)
        if client:
            print('| {:<8} | {:>10} | {:>15} | {:>25} | {:>20} |'.format(
                'ID', 'NAME', 'COMPANY', 'EMAIL', 'POSITION'))
            print('-' * 94)
            print('| {:<8} | {:>10} | {:>15} | {:>25} | {:>20} |'.format(
                id, client['name'], client['company'], client['email'], client['position']))
        else:
            print(f'{client_name} does not exist')

    elif command == 'L':
        list_clients()
    elif command == 'E':
        _exit_program()
    else:
        print('Invalid command')

    _save_clients_to_storage()


if __name__ == "__main__":
    main()
