import pymongo
import redis
import json


def save():
    redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
    mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)

    collection = mongo_client['tencent']['tencent_redis']

    while True:
        item = redis_client.lpop('tencent_redis:items')
        try:
            collection.insert(json.loads(item.decode()))
        except AttributeError:
            pass


if __name__ == '__main__':
    save()
