import boto.dynamodb
conn = boto.dynamodb.connect_to_region('us-west-2', aws_access_key_id="AKIAJIZEDKWEAUO6ZRPQ", aws_secret_access_key="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")

import json
from pprint import pprint

#creating tables

table=conn.get_table('user_info')

with open('yelp_academic_dataset_user.json') as data_file:
        key='user_id'
        item_data={'friends':data1['friends']}
        item=table.new_item(
        hash_key=data1['user_id'],
        attrs=item_data)
        item.put()


table=conn.get_table('business')

with open('yelp_academic_dataset_business.json') as data_file:
        key='business_id'
        item_data={'categories':data1['categories'],'hours':data1['hours'],'latitude
':data1['latitude'],'longitude':data1['longitude'],'stars':data1['stars']} 
        
        item=table.new_item(
        hash_key=data1['business_id'],
        attrs=item_data)
        item.put()


