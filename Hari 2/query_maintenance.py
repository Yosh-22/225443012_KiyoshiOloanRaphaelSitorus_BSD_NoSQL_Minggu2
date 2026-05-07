import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["latihan6"]
collection = db["maintenance"]

# =========================
# 1. QUERY BIAYA > 1.000.000
# =========================
cursor = collection.find({"biaya": {"$gt": 1000000}}, {"_id": 0})
df = pd.DataFrame(list(cursor))

print("Data biaya > 1 juta:")
print(df)

# =========================
# 2. UPDATE DATA
# =========================
update_result = collection.update_one(
    {"mesin": "CNC-01", "biaya": 1200000},
    {"$set": {"teknisi": "Dewi"}}
)

print(f"Data diupdate: {update_result.modified_count}")

# =========================
# 3. AGREGASI TOTAL BIAYA PER BULAN
# =========================
pipeline = [
    {
        "$group": {
            "_id": {
                "bulan": {"$month": "$tanggal"},
                "tahun": {"$year": "$tanggal"}
            },
            "total_biaya": {"$sum": "$biaya"},
            "jumlah_data": {"$sum": 1}
        }
    },
    {"$sort": {"_id.tahun": 1, "_id.bulan": 1}}
]

hasil = list(collection.aggregate(pipeline))

df_agregasi = pd.DataFrame(hasil)

print("\nTotal biaya per bulan:")
print(df_agregasi)

client.close()