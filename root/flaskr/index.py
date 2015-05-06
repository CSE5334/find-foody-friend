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
from flask import request
from flask import jsonify
import json,ast
import hashlib


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
    
#@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return request.remote_addr

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    users, restaurants = connect_db()
    record = None
    if request.method == 'POST':#Get logged in user information
        record = users.find_one({'_id': request.form['username'],'password':request.form['username']})
        if not record:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('Login successful')
            IP = get_my_ip()
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
            session['latitude']=data['latitude']
            session['longitude']=data['longitude']
            session['city']=data['city']
            session['state']=data['region_code']
            session['userData']= record
            print data['latitude']
            print data['longitude']
            print data['city']
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
    return render_template('location.html', error = error)
    
@app.route('/location')
def location():
    print "location"
    error =[]
    IP = get_my_ip()
    print(IP)
    rawdata = pygeoip.GeoIP('../GeoLiteCity.dat')
    data = rawdata.record_by_name(IP)
    latitude=data['latitude']
    longitude=data['longitude']
    print(latitude)
    print(longitude)
    
    return render_template('location.html', error = error,latitude=latitude,longitude=longitude)

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
    entries = []
    rest_count={}
    categories = collections.Counter()
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
                    categories[k]+=int(v)
                    if k in dict1:
                        #Use Manhattan distance to find the user match
                        score+= abs(v - dict1[k])
                        result[doc['name']] = score
                        cat_list.append(k)
                        fcat.append(k)
                cat_ulist[doc['name']] = list(set(cat_list))
            #Bring the restaurants ids for the each matched category
                
        sorted_result = sorted(result.items(), key =operator.itemgetter(1))
        if len(sorted_result) > 2:#Fetch only top three matched users.
            entries = [value[0] for value in sorted_result[:3]]
        else:
            entries = [value[0] for value in sorted_result]
            
    #remove duplicates from the categories by converting list to set
    fcat = list(set(fcat))
    fcat.remove('Restaurants')
    cat_res = {}
    r_data={}
    #for each category fetch the number of restaurants from the database.
    #Looping through database might pose a significant performance issue but
    #on cloud since EC2 data is where webpage is hosted doesnt take much time.
    for cat in fcat:
        rest_cursor = restaurants.find({'city': city, 'category':cat})
        if rest_cursor.count() ==0: #If no restaurant with the caterogy
            continue
        else:
            rest_count[cat]=rest_cursor.count()#count no. of restaurants per category
            ids=[]
            for row in rest_cursor:
                if (row['open'] == "{}"):#check if open hours info available
                    open_hours = "Open Hours: Info. not available"
                else:
                    open_hours = "Open Hours:" + row['open']
                    #Append the address and the restaurant open hours timings
                ids.append(row['address'] + '\n'+ open_hours)
            cat_res[cat]=ids
    #update the restaurant data against each matched user.  
    for k,v in cat_ulist.items():
        pf_cat = {}
        for item in v:
            if item in cat_res:
                pf_cat[item]=cat_res[item]
        rest_result[k]=pf_cat
    
    rests =  [dict(name=k, value=v)for k,v in rest_result.items()]
    result.clear()
    fusers= []
    session['category'] = categories
    session['rest_count'] = rest_count
    return render_template('show_users2.html', entries = entries, rests=rests, categories = categories, rest_count=rest_count)

@app.route('/graph_data')#to draw graph data
def graph_data(chartID='chart_ID', chart_type = 'pie', chart_height=300):
#def graph_data():
    cat_list=[]
    rest_list=[]
    pageType = 'graph'
    title = {'text':'Category percent in the Area'}
    category = session.get('category')
    restCount = session.get('rest_count')
    for k,v in category.items():
        cat_list.append([k,int(v)])
    #series = [{'type':'pie', 'name':'Category distribution', 'data':cat_list}]
    series = ast.literal_eval(json.dumps(cat_list))

    for k,v in restCount.items():
        rest_list.append([k,int(v)])
    rests = ast.literal_eval(json.dumps(rest_list))
  
    
    return render_template('show_gchart.html',pageType = pageType, chartID=chartID,title = title, series=series,rests=rests)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
