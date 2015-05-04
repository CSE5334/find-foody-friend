#!/usr/bin/env python
import sys
import re
import csv

list = []
const_one = '1'
for line in sys.stdin:
	row = line.strip().split('\t')
	#print row[3]
	categories = row[3].replace('"','')
	categories = row[3].replace("[","")
	categories = categories.replace("]","")
	categories = categories.replace("u'","")
	categories = categories.replace("'","")
	categories = categories.replace('"','')
	list_cat = categories.strip().split(",")
	for category in list_cat:
		print ('%s\t%s\t%s' % (row[0],category.strip(),const_one))

