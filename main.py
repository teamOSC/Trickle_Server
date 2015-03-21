import flask
from flask_oauth import OAuth
from flask import request
from datetime import datetime
import json
import requests

app = flask.Flask(__name__)

def get_dict(**kwargs):
    d= {}
    for k,v in kwargs.iteritems():
        d[k] = v
    return d

def scrape():
    with open("data/hotels.json",'r') as f:
        data = f.read()
        data = json.loads(data)

    arr = []
    for i in data["data"]:
        i.append(geocode_(i[0]+" "+i[1]))
        dict = get_dict(name=i[1],address=i[2],state=i[3],phone_1=i[4],phone_2=i[5],\
        mail_1=i[6],mail_2=i[7],type=i[8],rooms=i[9])
        arr.append(dict)
        print dict

    with open("data/hotels_.json",'r') as f:
        f.write(json.dumps(arr))
    
    return ""


def geocode_(address):
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyAnFWncNFX_cgSOqUUR7u5udupNPrkQ0Ro"%address
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
    with open("data/hotels.json",'r') as f:
        data = f.read()

    return json.dumps(data)

@app.route('/geocode',methods=['GET'])
def geocode():
    address = request.args.get('address')
    return json.dumps(geocode_(address))


if __name__ == '__main__':
    scrape()
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
