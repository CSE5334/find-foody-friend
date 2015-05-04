#all imports

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import pymongo
import hashlib
from pymongo import MongoClient
#from pymongo import ReturnDocument
import ipgetter
import pygeoip
import operator
import collections

DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    client = MongoClient('localhost', 27017)
    db = client.yelp_data
    return db.users

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    users = connect_db()
    record = None
    if request.method == 'POST':
        record = users.find_one({'_id': request.form['username']})
        if not record:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('Login successful')
            IP = ipgetter.myip()
            rawdata = pygeoip.GeoIP('C:\\Users\\HarshaVardhan\\Desktop\\DM final\\GeoLiteCity.dat')
            data = rawdata.record_by_name(IP)
            users.update(
                {'_id': request.form['username']},
                {'$set':{'latitude': data['latitude'],
                          'longitude': data['longitude'],
                           'city': data['city']}
                  }
                )
            session['city']=data['city']
            session['userData']= record
            return redirect(url_for('show_users'))
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/')
def fun():
    print "hello"
    return 'Hello'
    

@app.route('/users')
def show_users():
    users = connect_db()
    city = session.get('city')
    user = session.get('userData')
    cursor = users.find({'city': city})
    dictu=user['highrating']
    result = {}
    fusers = []
    entries = {}
    
    for doc in cursor:
        #if (doc['_id'] == user['_id']):
         #   continue
        #else:
        dict1 = doc['highrating']
        score = 0
        for k,v in dictu.items():
            if k in dict1:
                score+= abs(v - dict1[k])
                result[doc['name']] = score
        #sorted_result = sorted(result.items(), key =operator.itemgetter(1))
        #fresult = collections.Counter(result)
        entries = [dict(name=k, value=v)for k,v in result.items()]
        result.clear()
        fusers= []
        sorted_results={}
    print entries
    return render_template('show_users.html', entries = entries)

if __name__ == '__main__':
    app.run()
