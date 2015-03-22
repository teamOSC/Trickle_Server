
from bs4 import BeautifulSoup
import requests
import json
import ast

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
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyCJ8YcVRi3v0wbpUszPeGwF-E1O1LBVL68"%address
    r = requests.get(geocoding_url).json()
    #coords = r["results"]["geometry"]["location"]
    try:
        coords = r["results"][0]["geometry"]["location"]
    except IndexError:
        coords=""


    return coords

def get_dict(**kwargs):
    d= {}
    for k,v in kwargs.iteritems():
        d[k] = v
    return d

def scrape_census():
    url ='http://www.census2011.co.in/district.php'
    soup = BeautifulSoup( requests.get(url).text )
    main_arr=[]
    for i in soup.select(".table .row"):
        for j in i.select(".cell")[1:]:
            try:
                text = i.get_text()
                a=[i for i in text.split("\n") if i][1:]
                main_arr.append(a)
            except AttributeError:
                pass

    arr = []
    for i in main_arr:
        coords= geocode_(i[0]+" "+i[1])
        #coords=""
        d = get_dict(coords=coords,district=i[0],state=i[1],population=i[2],growth=i[3],sex_ratio=i[4],literacy=i[5])
        arr.append(d)
        #print d

    print json.dumps(arr)
    with open('data/heat1.json','w+') as f:
        f.write(json.dumps(arr))

def adler():
    qt = "How deep is grand canyon ?"
    d={"question":{"questionText":qt,"evidenceRequest":{"items":1}}}
    url ="https://gateway.watsonplatform.net/question-and-answer-beta/api/v1/question/travel"
    print type(json.dumps(d))
    print type(ast.literal_eval(json.dumps(d)))
    #print type(json.loads(d))
    r = requests.post(url,
        data=json.dumps(d),
        headers={'Accept':'application/json','Content-Type':'text/json','X-SyncTimeout':'30'},
        auth=('fe4fa332-50cb-4c91-9ce5-84122b753824','swKJrtrfi8fS')
        )
    try:
        print r.text
    except:
        pass

def foo():
    with open("data/heat1.json") as f:
        data = json.loads(f.read())
    max = 0
    for i in data:
        p = int(i['population'].replace(',',""))
        if p>max:
            max = p
    for i in data:
        i['percent'] = int(i['population'].replace(",",""))/float(max)
        print i,i['percent'],max

    with open('data/heat2.json','w+') as f:
        f.write(json.dumps(data))
    

def foo2():
    with open ('data/pollution.json') as f:
        data = json.loads(f.read())
    arr=[]
    for i in data['data']:
        d={}
        d['state'] = i[0]
        d['level'] = i[-1]
        d['coords'] = geocode_(i[0]+' india')
        arr.append(d)

    with open('data/pollution_.json','w+') as f:
        f.write(json.dumps(arr))

if __name__ == '__main__':
    adler()
    #foo2()
    #scrape_census()
