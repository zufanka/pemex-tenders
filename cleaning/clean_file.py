# -*- coding: utf-8 -*-

import csv, datetime, urllib, simplejson, requests

def Inflation(y, rates):

    rate = 1
    while y < 2015:
        rate = rate+(rate*(rates[y+1]))
        y += 1

    return rate

def BestMatch(json):

#    print json

    try:
        bm = json['result'][0]
        url = "https://api.opencorporates.com" + bm['id']

        match = simplejson.load(urllib.urlopen(url))
        
        return match['results']['company']['name'], match['results']['company']['jurisdiction_code'], match['results']['company']['company_number']

    except IndexError:
        return "nomatch","nomatch","nomatch"
        


# calculate inflation rate per 1 pesos (dec 2015), source: https://www.statbureau.org/en/mexico/inflation-tables

inputfile = open("yoy-inflation-2001-2015.csv")
reader = csv.reader(inputfile)

reader.next()
yoy = dict((int(r[0]),round(float(r[1])/100,4)) for r in reader) # change the inflation from % to float

inflation = {}
for year in xrange(2001,2016):
    inflation[year] = Inflation(year, yoy)

#input file
inputfile = open("../pemextest.csv")
pemex = csv.reader(inputfile)

suppliers = {}

pemex.next()
for row in pemex:

    # fix inflation
    awardyear = int((row[5]).split('/')[2])
    currency = row[7]

    pesos = round((float(row[8]) * inflation[awardyear]),3)

    if currency == "DOLAR":
        pesos = pesos * float(row[9])

    # fix double entries -- need to check with the source!

    # fix multiple companies per row

    #
    # clean company strings
    #

        # reconcile API, example: http://onlinejournalismblog.com/tag/opencorporates/

    sname = row[4]

    try:
        cname = suppliers[sname]['name']
        country = suppliers[sname]['country']
        id = suppliers[sname]['id']
            
    except KeyError:

        url = "https://opencorporates.com/reconcile/?query="+urllib.quote(sname)
        entities = simplejson.load(urllib.urlopen(url))
        cname, country, id = BestMatch(entities)

        suppliers[sname] = {}
        suppliers[sname]['name'] = cname
        suppliers[sname]['country'] = country
        suppliers[sname]['id'] = id

    print awardyear,sname, cname, country, id
            
           
