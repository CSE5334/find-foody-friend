import json
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.yelp_data
users = db.users

with open('resulthigh.json') as low_file:
    data = json.load(low_file)

for key,value in data.items():
    record = users.find_one({'_id': key})
    if not record:
        continue
    else:
        users.update(
            {'_id': key},
            {'$set':{'highrating':value}
             }
            )

print 'update done'
    
