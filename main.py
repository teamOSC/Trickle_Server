import flask
#from flask_oauth import OAuth
from flask import request
from datetime import datetime
import json
import requests
from flask import jsonify
import math

app = flask.Flask(__name__)

def get_dict(**kwargs):
    d= {}
    for k,v in kwargs.iteritems():
        d[k] = v
    return d


@app.route('/', methods=['GET'])
def home():
    map_long = request.args.get('long')
    map_lat = request.args.get('lat')
    map_type = request.args.get('type')
    radius = request.args.get('radius') or 2000
    map_type = map_type.replace(",","|")

    with open("data/service__.json",'r') as f:
        data = json.loads(f.read())

    for i in data:
        print i
        i['dist'] = math.hypot(float(map_lat) - float(i['coords']['lat']), float(map_long) - float(i['coords']['lng']))

    services = sorted(data, key=lambda k: k['dist']) 
    
    url = "https://maps.googleapis.com/maps/api/place/search/json?types=%s&location=%s,%s&radius=%s&key=AIzaSyDLKMcL0I-b3X_jOiCtdjEI2hDkT5B6J8g"%(map_type,map_lat,map_long,radius)
    
    r = requests.get(url).json()['results']
    arr=[]
    for i in r:
        try:
            dict = get_dict(rating=i['rating'],name=i['name'],
                coords=i['geometry']['location'],meta="")
        except KeyError:
            dict = get_dict(rating='',name=i['name'],
                coords=i['geometry']['location'],meta="")
        arr.append(dict)

    if 'hotels' not in map_type:
        return jsonify(data = arr,services=services)

    with open("data/hotels__.json",'r') as f:
        data = json.loads(f.read())

    for i in data:
        print i
        i['dist'] = math.hypot(float(map_lat) - float(i['coords']['lat']), float(map_long) - float(i['coords']['lng']))

    hotels = sorted(data, key=lambda k: k['dist'])

    return jsonify(data = arr,hotels=hotels,services=services)
        

@app.route('/heat',methods=['GET'])
def heat():
    map_lat = request.args.get('lat')
    map_long = request.args.get('long')
    heat_type = request.args.get('type')
    count = request.args.get('count') or '10'
    count = int(count)

    with open ('data/heat2.json') as f:
        data = json.loads(f.read())

    arr_w = []
    for i in data:
        try:
            i['dist'] = math.hypot(float(map_lat) - float(i['coords']['lat']), float(map_long) - float(i['coords']['lng']))
            arr_w.append(i)
        except:
            pass
    
    heat = sorted(arr_w, key=lambda k: k['dist'])
    
    return json.dumps(heat[:count])

@app.route('/adler',methods=['GET'])
def question():
    q = request.args.get('q')
    return jsonify(response="Hello World")

@app.route('/geocode',methods=['GET'])
def geocode():
    address = request.args.get('address')
    return json.dumps(geocode_(address))

    


if __name__ == '__main__':
    #scrape_service()
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
