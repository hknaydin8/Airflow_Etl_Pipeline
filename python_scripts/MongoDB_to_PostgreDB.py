from sqlalchemy import create_engine
import pandas as pd
import pymongo


# PostgreSQL bağlantısı
pg_engine = create_engine('postgresql+psycopg2://airflow:airflow@postgresql:5432/postgres')


# MongoDB bağlantısı
client = pymongo.MongoClient("mongodb://mongo:27017/", username="admin", password="admin")
db = client["MyTestdb"]
shipment_collection = db["Shipment"]


# MongoDB'den verileri al
mongo_shipments = list(shipment_collection.find())

# Eğer veri yoksa, uyarı ver ve işlemi sonlandır
if not mongo_shipments:

    print("No data found in the 'Shipment' collection.")

else:
    df = pd.DataFrame(mongo_shipments)

    def get_parcel_id(parcels):
        return [parcel["parcel_id"] for parcel in parcels]

    # parcels içindeki parcel_id'yi almak için bir fonksiyon tanımlayın
    # parcel_id sütununu oluşturun
    df["parcel_id"] = df["parcels"].apply(get_parcel_id)

    df_shipment = df[['shipment_id', 'shipment_date', 'parcel_id', 'shipment_status', 'shipment_store', 'tracking_number']]

    def extract_parcel_info(parcels):
        parcel_info = []
        for parcel in parcels:
            parcel_id = parcel["parcel_id"]
            barcodes = parcel["barcodes"]
            package_name = parcel["package_name"]
            sizes = parcel["sizes"]
            for barcode, package_size in zip(barcodes, sizes):
                parcel_info.append({"parcel_id": parcel_id, "barcode": barcode, "package_name": package_name, "package_size": package_size})
        return parcel_info

    # DataFrame'deki parça detaylarını ayrıştırma
    parcel_info = df["parcels"].apply(extract_parcel_info).explode()
    # Parça DataFrame'i oluşturma
    df_parcel = pd.DataFrame(parcel_info.tolist())

    def extract_address_info(row):
        return {
            "shipment_id": row["shipment_id"],
            "street": row["address"]["street"],
            "district": row["address"]["district"],
            "city": row["address"]["city"],
            "country": row["address"]["country"],
            "zip_code": row["address"]["zip_code"]
        }

    # Adres bilgilerini içeren yeni bir DataFrame oluşturma
    df_address = pd.DataFrame(df.apply(extract_address_info, axis=1).tolist())
def transfer_data():

    # Verileri PostgreSQL tablolarına yaz
    df_shipment.to_sql('shipment', pg_engine, if_exists='replace', index=False)
    df_parcel.to_sql('shipment_parcel', pg_engine, if_exists='replace', index=False)
    df_address.to_sql('shipment_address', pg_engine, if_exists='replace', index=False)

    print("Data transfer completed.")

transfer_data()

