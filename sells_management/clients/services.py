import csv
import os
from clients.models import Client
class ClientService:
    def __init__(self, table_name):
        self.table_name = table_name

    def create_client(self, client):
        with open(self.table_name, mode='a') as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerow(client.to_dict())

    def list_clients(self):
        with open(self.table_name, mode='r') as f:
            reader = csv.DictReader(f, fieldnames=Client.schema())
            return list(reader)

    def update_client(self, updated_client):
        clients = self.list_clients()
        updated_clients = list(map(lambda client: updated_client.to_dict() if client['uid'] == updated_client.uid else client, clients))
        self._save_clients(updated_clients)
    
    def delete_client(self, client):
        clients = self.list_clients()
        clients = list(filter(lambda c: c['uid'] != client.uid, clients))
        self._save_clients(clients)
        
    def _save_clients(self, clients):
        tmp_table_name = self.table_name + '.tmp'
        with open(tmp_table_name, mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerows(clients)
        
        os.remove(self.table_name)
        os.rename(tmp_table_name, self.table_name)
    