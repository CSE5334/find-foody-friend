#!/usr/bin/env python
import sys
import re
import json
rating ={}
for line in sys.stdin:
    key1,key2,value = line.strip().split('\t')
    try:
        value = int(value)
    except ValueError:
        continue
    if key1 in rating:
        category = rating[key1]
        category[key2] = value
    else:
        rating[key1] = {}

with open('resulthigh.json','w') as fp:
	json.dump(rating,fp)
            
        
        
