import os

import ipgetter
import pygeoip
IP = ipgetter.myip()
'''rawdata = pygeoip.GeoIP('C:\\Users\\HarshaVardhan\\Desktop\\DM final\\GeoLiteCity.dat')
data = rawdata.record_by_name(IP)'''
from urllib import urlopen, quote
import simplejson

GEOIP_LOOKUP_URL = 'http://ipinfodb.com/ip_query.php?ip=%s&output=json'

def geo_ip_lookup(ip_address):
    """
    Look up the geo information based on the IP address passed in
    """
    lookup_url = GEOIP_LOOKUP_URL % ip_address
    json_response = simplejson.loads(urlopen(lookup_url).read())

    return {
            'country_code': json_response['CountryCode'],
            'country_name': json_response['CountryName'],
            'locality': json_response['City'],
            'region': json_response['RegionName'],
            'longitude': json_response['Longitude'],
            'latitude': json_response['Latitude']
    }
print geo_ip_lookup(IP)

