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

    with open("data/hotels_.json",'w+') as f:
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

@app.route('/qa',methods=['GET'])
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
    return ""

def test():
    qt = 'How deep is grand canyon ?'
    headers={}
    url ="https://gateway.watsonplatform.net/question-and-answer-beta/api/v1/question/travel"
    r = requests.post(url,
        data={'question':{'questionText':qt,'evidenceRequest':{'items':1}}},
        headers={'Accept':'application/json','Content-Type':'text/json','X-SyncTimeout':'30'},
        auth=('fe4fa332-50cb-4c91-9ce5-84122b753824','swKJrtrfi8fS')
        )
    print r
    try:
        print r.text
    except:
        pass


if __name__ == '__main__':
    test()
    #app.debug = True
    #app.run(host='0.0.0.0', port=8000)
