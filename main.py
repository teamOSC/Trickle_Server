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

def scrape_service():
    with open("data/service.json",'r') as f:
        data = f.read()
        data = json.loads(data)

    arr = []
    for i in data["data"]:
        lat_lang=geocode_(i[0]+" "+i[1])
        if not lat_lang:
            continue
        dict = get_dict(name=i[0],coords=lat_lang,meta="Phone: %s , Contact: %s , Mail: %s"%(i[2],i[8],i[4]),rating="")
        arr.append(dict)
        print dict

    with open("data/service__.json",'w+') as f:
        f.write(json.dumps(arr))
    
    return ""

def scrape_hotels():
    with open("data/hotels.json",'r') as f:
        data = f.read()
        data = json.loads(data)

    arr = []
    for i in data["data"]:
        lat_lang=geocode_(i[0]+" "+i[1])
        if not lat_lang:
            continue
        dict = get_dict(name=i[0],coords=lat_lang,meta="Phone: %s ,Mail: %s , Type: %s, Rooms: %s"%(i[3],i[5],i[7],i[8]),rating="")
        arr.append(dict)
        print dict

    with open("data/hotels__.json",'w+') as f:
        f.write(json.dumps(arr))
    
    return ""

def geocode_(address):
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyDmUUwc54w3uoNlGXenMR5oNzm3qTRVbtY"%address
    r = requests.get(geocoding_url).json()
    #coords = r["results"]["geometry"]["location"]
    try:
        coords = r["results"][0]["geometry"]["location"]
    except IndexError:
        coords=""
    return coords

@app.route('/', methods=['GET'])
def home():
    map_long = request.args.get('long')
    map_lat = request.args.get('lat')
    map_type = request.args.get('type')

    with open("data/hotels__.json",'r') as f:
        data = json.loads(f.read())

    for i in data:
        print i
        i['dist'] = math.hypot(float(map_lat) - float(i['coords']['lat']), float(map_long) - float(i['coords']['lng']))

    hotels = sorted(data, key=lambda k: k['dist']) 

    with open("data/service__.json",'r') as f:
        data = json.loads(f.read())

    for i in data:
        print i
        i['dist'] = math.hypot(float(map_lat) - float(i['coords']['lat']), float(map_long) - float(i['coords']['lng']))

    services = sorted(data, key=lambda k: k['dist']) 
    
    url = "https://maps.googleapis.com/maps/api/place/search/json?types=%s&location=%s,%s&radius=5000&key=AIzaSyDLKMcL0I-b3X_jOiCtdjEI2hDkT5B6J8g"%(map_type,map_lat,map_long)
    #return url
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

    return jsonify(data = arr,hotels=hotels,services=services)

@app.route('/geocode',methods=['GET'])
def geocode():
    address = request.args.get('address')
    return json.dumps(geocode_(address))

@app.route('/assistant',methods=['GET'])
def question():
    qt = 'How far is kashmir from Delhi ?'
    headers={}
    url ="https://gateway.watsonplatform.net/question-and-answer-beta/api"
    r = requests.post(url,
        data={'questionText':qt},
        headers={'Accept':'application/json',"X-SyncTimeout":'30'},
        auth={'fe4fa332-50cb-4c91-9ce5-84122b753824','swKJrtrfi8fS'},
        )
    print r.text
    return jsonify(response="Hello World")
    

def wattson():
    qt = 'How deep is grand canyon ?'
    url ="https://gateway.watsonplatform.net/question-and-answer-beta/api/v1/question/travel"
    r = requests.post(url,
        data={'question':{'questionText':qt,'evidenceRequest':{'items':1}}},
        headers={'Accept':'application/json','Content-Type':'text/json','X-SyncTimeout':'30'},
        auth={'fe4fa332-50cb-4c91-9ce5-84122b753824','swKJrtrfi8fS'}
        )
    print r
    try:
        print r.text
    except:
        pass


if __name__ == '__main__':
    #scrape_service()
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
