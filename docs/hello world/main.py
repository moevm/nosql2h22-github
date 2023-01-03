from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["SampleBD"]

collection_name = input("Collection name: ")
data = input("Data: ")

collection = mydb[collection_name]
insert_data = collection.insert_one({"Data": data})

for coll in mydb.list_collection_names():
    print(coll + ":")
    for data in mydb[coll].find():
        print(" " + str(data))