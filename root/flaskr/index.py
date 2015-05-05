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
from flask_bootstrap import Bootstrap

DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

def connect_db():
    client = MongoClient('localhost', 27017)
    db = client.yelp_data
    return db.users, db.restaurants

def get_rest_list(category,restaurant_list):
    ids = {}
    for row in restaurant_list:
        if category in row['category']:
            ids['_id'] = row['rating']
    sorted_rest = sorted(ids.items(), key =operator.itemgetter(1))
    #print sorted_rest
    if len(sorted_rest) > 1:
        return sorted_rest[:2]
    else:
        return sorted_rest
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    users, restaurants = connect_db()
    record = None
    if request.method == 'POST':
        record = users.find_one({'_id': request.form['username']})
        if not record:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('Login successful')
            IP = ipgetter.myip()
            rawdata = pygeoip.GeoIP('../GeoLiteCity.dat')
            data = rawdata.record_by_name(IP)
            users.update(
                {'_id': request.form['username']},
                {'$set':{'latitude': data['latitude'],
                          'longitude': data['longitude'],
                           'city': data['city'],
                            'state': data['region_code']}
                  }
                )
            session['city']=data['city']
            session['state']=data['region_code']
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
    error = None
    return render_template('temp2.html', error = error)
    

@app.route('/users')
def show_users():
    users, restaurants = connect_db()
    city = session.get('city')
    state = session.get('state')
    user = session.get('userData')
    cursor = users.find({'city': city})
    
    
    dictu=user['highrating']
    result = {}
    rest_result = {}
    fcat = []
    cat_ulist={}
    cat_list=[]
    for doc in cursor:
        if (doc['_id'] == user['_id']):
            continue
        else:
            if 'highrating' not in doc:
                continue
            else:
                dict1 = doc['highrating']
                score = 0
                for k,v in dictu.items():
                    if k in dict1:
                        score+= abs(v - dict1[k])
                        result[doc['name']] = score
                        cat_list.append(k)
                        fcat.append(k)
                cat_ulist[doc['name']] = list(set(cat_list))
            #Bring the restaurants ids for the each matched category
                
        sorted_result = sorted(result.items(), key =operator.itemgetter(1))
        #fresult = collections.Counter(result)
    fcat = list(set(fcat))
    fcat.remove('Restaurants')
    cat_res = {}
    r_data={}
    for cat in fcat:
        rest_cursor = restaurants.find({'city': city, 'category':cat})
        if rest_cursor.count() ==0:
            continue
        else:
            ids=[]
            for row in rest_cursor:
                r_data[row['_id']] = row
                ids.append(row['_id'])
            cat_res[cat]=ids
      
    for k,v in cat_ulist.items():
        pf_cat = {}
        for item in v:
            if item in cat_res:
                pf_cat[item]=cat_res[item]
        rest_result[k]=pf_cat
    
    rests =  [dict(name=k, value=v)for k,v in rest_result.items()]
    #print r_data
    #entries = [dict(name=k, value=v)for k,v in dict(sorted_result).items()]
    result.clear()
    fusers= []
    #print sorted_result
    
    return render_template('show_users.html', entries = sorted_result[:2], rests=rests)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
