import redis
from pymongo import MongoClient
import json


def main():
    r = redis.Redis(host='localhost', port=6379, db=0)
    redis_data = r.get('foo')
    data = json.loads(redis_data)

    client = MongoClient('localhost', 27017)
    db = client.test_database
    collection = db.test_collection

    collection.insert_one(data)    

if __name__ == "__main__":
    main()