import pymongo
from pymongo import MongoClient
from urllib2 import urlopen
import json

client = MongoClient('localhost', 27017)
db = client.yelp_data
restaurants = db.restaurants

def getCity(lat, lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if ("postal_town" in c['types']) or ("locality" in c['types']):
            town = c['long_name']
    return town
enc = "latin-1"

f = open("up_data.txt","r")
for line in f:
    content = line.decode(enc)
    utf8_content = content.encode("utf8")
    data = utf8_content.strip().split('\t')
    categories = data[6].replace("[","")
    categories = categories.replace("]","")
    categories = categories.replace("u'","")
    categories = categories.replace("'","")
    categories = categories.replace('"','')
    list_cat = categories.strip().split(",")
    
    open_hours = data[5].replace("u'","")
    open_hours = open_hours.replace("'","")
    
    item_data = {
        '_id':data[0],
        'address':data[2],
        'city':data[1],
        'open':open_hours,
        'category':list_cat,
        'state':data[8],
        'rating':data[7]
        }
    restaurants.insert(item_data,safe=True)
        
f.close()
