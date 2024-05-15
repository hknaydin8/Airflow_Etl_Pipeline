import json
import os
import pymongo

data_directory = os.path.dirname(__file__)
file_path = os.path.join(data_directory, "Shipments_Data.json")

# MongoDB bağlantısı
client = pymongo.MongoClient("mongodb://mongo:27017/", username="admin", password="admin")
db = client["MyTestdb"]
shipment_collection = db["Shipment"]



# Tüm mevcut gönderileri silme
def delete_all_shipments():
    result = shipment_collection.delete_many({})
    print("Deleted", result.deleted_count, "shipments from the collection.")

# JSON dosyasından verileri okuyarak MongoDB'ye ekleme
def insert_shipment_collection_mongodb():
    with open(file_path, 'r') as json_file:
        shipments = json.load(json_file)
        result = shipment_collection.insert_many(shipments)
    print("Shipments added with IDs:", result.inserted_ids)

# Fonksiyonları çağır
delete_all_shipments()
insert_shipment_collection_mongodb()
