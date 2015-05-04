import json
from pprint import pprint
#import boto.dynamodb
import pymongo
import hashlib
from pymongo import MongoClient

'''conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id= 'AKIAJEALAHGUNLPJCXYQ',
        aws_secret_access_key= '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')
table = conn.get_table('users')'''

client = MongoClient('localhost', 27017)
db = client.yelp_data
users = db.users
with open('yelp_academic_dataset_user.json') as data_file:
    for line in data_file:
        data = json.loads(line)
        hash_pswd = hashlib.md5(data['yelping_since'].encode())
        if data['friends']:
            list_f = data['friends']
        item_data = {
            '_id': data['user_id'],
            'name': data['name'],
            'friends': list_f,
            'password': str(hash_pswd)
            }
        users.insert(item_data,safe=True)
        '''item = table.new_item(
            #hash key userId
            hash_key = data['user_id'],
            attrs = item_data
            )
        item.put()'''

print 'done'
