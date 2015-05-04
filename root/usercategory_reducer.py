#!/usr/bin/env python
import sys
import re

count = 0
current_key = None
for line in sys.stdin:
	key1,key2,value = line.strip().split('\t')
	key = key1+"\t"+key2
	try:
        	value = int(value)
	except ValueError:
        	continue
    	if (key == current_key):
        	count+=value
    	else:
        	if current_key:
            		print('%s\t%s' % (key,count))
            	count = value
            	current_key = key
        
if current_key:
	print('%s\t%s' % (key,count))
