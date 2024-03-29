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

@app.route('/pollution')
def pollution():
    with open ('data/pollution_.json') as f:
        data = json.loads(f.read())
    return jsonify(data=data)



@app.route('/adler',methods=['GET'])
def question():
    q = request.args.get('q')
    resp = chat(q)
    return json.dumps(resp)
    if 'dharamshala' in q:
        resp = """
        Many people take a taxi to Delhi which takes about 10 hours and pay the return fare simply because they don't want to deal with the hassle and pain of taking a bus. These taxis need to return to Dharamshala, and many times will sell seats in their car for the same price as a bus ticket. To find these taxis, go to the Majnu Ki Tila Tibetan Settlement Bus Stand and look for taxis which have Himachal Pradesh License plates. You can negotiate with a driver.
        """
    if 'manali' in q:
        resp = """
        Booking Delhi Manali BUS Tickets is easily done with MakeMyTrip Online Bus Booking
Multiple payment options available - Credit Card/Debit Card/Cash Card or Online bank account
Please print your online Bus & Train Tickets and carry it while traveling
Multiple bus types are available such as Volvo, AC, Non AC, AC available between Delhi Manali
Also check bus fare and timings before making a reservation
- See more at: http://www.makemytrip.com/bus-tickets/delhi-manali-booking.html#sthash.hx7yZvIp.dpuf
        """
    if "goa" in q:
        resp = """
        people will tell you what most tourist literatures do: Best time to visit Goa is November to February. But my advice is to go in monsoon. It is lush green, there is no tourist crowd the way it is in winter and most importantly, you will get dirt cheap holiday packages from amongst a whole range of options.
        """

    return jsonify(response=resp)
    
@app.route('/geocode',methods=['GET'])
def geocode():
    address = request.args.get('address')
    return json.dumps(geocode_(address))

def chat(text):
    from chatterbotapi import ChatterBotFactory, ChatterBotType

    factory = ChatterBotFactory()

    bot1 = factory.create(ChatterBotType.CLEVERBOT)
    bot1session = bot1.create_session()

    bot2 = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
    bot2session = bot2.create_session()

    return bot2session.think(text);
    while (1):

        print 'bot1> ' + s

        s = bot2session.think(s);
        print 'bot2> ' + s

        s = bot1session.think(s);    


if __name__ == '__main__':
    #scrape_service()
    #print chat("How are you")
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
