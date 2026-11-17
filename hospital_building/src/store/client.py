from store.DuplicateKeyException import DuplicateKeyException
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os


class Client:

    def __init__(self):
        address = os.getenv('MONGO_HOSTNAME', "mongodb")
        port = int(os.getenv('MONGO_PORT', 27017))
        user = os.getenv('MONGO_USER', "root")
        password = os.getenv('MONGO_PASSWORD',"S3cure.Passw0rd")
        client = MongoClient(address, port,
                             username=user,
                             password=password)

        dbname = os.getenv('MONGO_DB',"health")
        self.__db = client[dbname]
        
        

    def insert(self, table_name, item):
        try:
            table = self.__db[table_name]
            item_id = table.insert_one(item).inserted_id
        except DuplicateKeyError as e:
            raise DuplicateKeyException(str(e))
        except Exception as e:
            raise DuplicateKeyException(str(e))

        return item_id

    def find_one(self, table_name, search):
        table = self.__db[table_name]
        
        return table.find_one(search)
    
    def find_one_and_sort(self, table_name, search, sort_key, descending = 1):
        table = self.__db[table_name]
        
        cur = table.find(search)
        if cur is not None:
            ret = table.find(search).sort(sort_key, descending).limit(1)
            for r in ret:
                return r
        return None

    def find_and_sort(self, table_name, search, sort_key, descending = 1):
        table = self.__db[table_name]
        
        cur = table.find(search)
        if cur is not None:
            ret = table.find(search).sort(sort_key, descending)
            return ret
        return None
    
    def find(self, table_name, search):
        table = self.__db[table_name]
        return table.find(search)
    
    def distinct_and_sort(self, table_name, search, distinct_key, sort_key):
        table = self.__db[table_name]
        return table.find(search).distinct({distinct_key: True}).sort({sort_key: True})
    
    def aggregate_and_sort(self, table_name, match, group_by, sort_key):
        table = self.__db[table_name]
        ret =  table.aggregate(
                [
                    { "$match" : match },
                    { "$sort" : sort_key },
                    {"$group" : group_by }
                ]
        )
        
        # for r in ret:
        #     return r
        return ret
    
    def count(self, table_name, search):
        table = self.__db[table_name]
        return table.count_documents(search)

    def delete_one(self, table_name, search):
        table = self.__db[table_name]
        return table.delete_one(search)
    
    def delete(self, table_name, search):
        table = self.__db[table_name]
        return table.delete_many(search)

    def update_one(self, table_name, search, changes):
        table = self.__db[table_name]
        return table.update_one(search, changes)

    def get_instance(self):
        return self.__db
    

