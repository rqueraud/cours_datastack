from pymongo import MongoClient

def main():

    client = MongoClient('localhost', 27017)
    db = client.test_database
    collection = db.test_collection

    pipeline = [
        
    ]  # TODO, with a $merge state at the end to create the materialized view
    collection.aggregate(pipeline)

if __name__ == "__main__":
    main()