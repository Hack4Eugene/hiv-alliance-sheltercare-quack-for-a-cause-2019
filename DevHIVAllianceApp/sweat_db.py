import pymongo
import random
import json
from bson.objectid import ObjectId
from DatabaseClasses.Encounter import Encounter
from DatabaseClasses.Client import Client


MONGO_URI = "mongodb+srv://sweat:sweat1234@cluster0-d2riz.mongodb.net/test"


class HivAllianceDb():
    def __init__(self):
        self.db = pymongo.MongoClient(MONGO_URI).sweat

    def get_encounter_by_id(self, encounter_id):
        """
            Args:
                encounter_id (str): a unique identifier for an encounter
            Returns:
                Encounter: an encounter object
                None: if no such encounter id exists
        """
        encounter_dict = self.db.encounters.find_one({"_id": ObjectId(encounter_id)})
        encounter = Encounter()
        encounter.Populate(encounter_dict)
        return encounter


    def insert_encounter(self, encounter):
        """
            Args:
                encounter (Encouter): an encounter object to be updated in the DB (it should exist)
            Returns:
                str: a unique id for the encounter
        """
        return self.db.encounters.insert(encounter.__dict__)


    def update_encounter(self, encounter):
        """
            Args:
                encounter (Encouter): an encounter object
            Returns:
                str: a unique id for the encounter
        """
        encounter_id = encounter._id
        encounter_dict = encounter.__dict__
        del encounter_dict["_id"]
        self.db.encounters.update_one({"_id": ObjectId(encounter_id)}, {"$set": encounter_dict})
        return encounter_id

    
    def get_client_by_id(self, client_id):
        """
            Args:
                client_id (str): a unique identifier for a person
            Returns:
                Client: a client object
                None: if no such client id exists
        """
        client_dict = self.db.clients.find_one({"_id": ObjectId(client_id)})
        client = Client()
        client.Populate(client_dict)
        client.client_id = client_id
        return client


    def insert_client(self, client):
        """
            Args:
                client (Client): a client object
            Returns:
                str: a unique id for the client
        """
        return self.db.clients.insert(client.__dict__)


    def update_client(self, client):
        """
            Args:
                client (Client): a client object to be updated
            Returns:
                str: a unique id for the client
        """
        client_id = client._id
        client_dict = client.__dict__
        del client_dict["_id"]
        self.db.clients.update_one({"_id": ObjectId(client_id)}, {"$set":client_dict})
        return client_id


    def get_encounters_by_client_id(self, client_id):
        encounters = []
        for encounter_dict in self.db.encounters.find({"client_id": client_id}):
            encounter = Encounter()
            encounter.Populate(encounter_dict)
            encounters.append(encounter)
            
        return encounters

    def get_all_encounters(self):
        """
            Args:
                None
            Returns:
                list: A list of all encounters currently in the database
            
        """
        encounters = []
        for encounter_dict in self.db.encounters.find():
            encounter = Encounter()
            encounter.Populate(encounter_dict)
            encounters.append(encounter)
            
        return encounters


    def get_all_clients(self):
        """
            Args:
                None
            Returns:
                list: A list of all clients currently in the database
        """
        clients = []
        for client_dict in self.db.clients.find():
            client = Client()
            client.Populate(client_dict)
            clients.append(client)
            
        return clients

    def generate_random_json(self, client_count, encounter_count):
        clients = []
        encounters = []

        for x in range(client_count):
            client = Client()
            client.Randomize()
            clients.append(client.__dict__)

        for x in range(encounter_count):
            encounter = Encounter()
            encounter.Randomize()
            encounters.append(encounter.__dict__)

        with open('RawData/initialDbData.json', 'w') as json_file:
            json.dump({ 'clients' : clients, 'encounters' : encounters}, json_file, indent=4, sort_keys=True, default=str)

    def initialize_from_json(self):
        self.db.encounters.drop()
        self.db.clients.drop()

        with open('RawData/initialDbData.json') as json_file:  
            json_db_entries = json.load(json_file)

            for client in json_db_entries['clients']:
                client_class = Client()
                client_class.Populate(client)
                self.insert_client(client_class)

            clients = list(self.db.clients.find())

            for encounter in json_db_entries['encounters']:
                randomClient = random.choice(clients)
                randomClientId = randomClient['_id']

                encounter['client_id'] = randomClientId

                encounter_class = Encounter()
                encounter_class.Populate(encounter)
                encounterId = self.insert_encounter(encounter_class)

                randomClient['encounter_ids'].append(encounterId)
                self.db.clients.update_one({"_id": ObjectId(randomClientId)}, {"$set":randomClient})

        client_count = len(self.get_all_clients())
        encounter_count = len(self.get_all_encounters())

        self.db.encounters.create_index([("_id", pymongo.ASCENDING)])
        self.db.clients.create_index([("_id", pymongo.ASCENDING)])

        print("Initialized DB with %s clients and %s encounters" % (client_count, encounter_count))

def main():
    db = HivAllianceDb()
    for encounter in db.get_all_encounters():
        print(encounter.__repr__())


if __name__ == "__main__":
    main()
