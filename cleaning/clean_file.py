# -*- coding: utf-8 -*-

import csv, datetime, urllib, simplejson

def Inflation(y, rates):

    rate = 1
    while y < 2015:
        rate = rate+(rate*(rates[y+1]))
        y += 1

    return rate

# calculate inflation rate per 1 pesos (dec 2015), source: https://www.statbureau.org/en/mexico/inflation-tables

inputfile = open("yoy-inflation-2001-2015.csv")
reader = csv.reader(inputfile)

reader.next()
yoy = dict((int(r[0]),round(float(r[1])/100,4)) for r in reader) # change the inflation from % to float

inflation = {}
for year in xrange(2001,2016):
    inflation[year] = Inflation(year, yoy)

# input file
inputfile = open("../pemex.csv")
pemex = csv.reader(inputfile)

# read reconciled data

newdata = []
newrow = []

pemex.next()
for row in pemex:

    aid = row[0]

    # fix inflation
    awarddate = row[5].split('/')
    ayear = int(awarddate[2])
    amonth = int(awarddate[1])
    aday = int(awarddate[0])
    
    currency = row[7]

    pesos = round((float(row[8]) * inflation[ayear]),3)

    if currency == "DOLAR":
        pesos = pesos * float(row[9])

    # procedure
    if row[2] == 'OTROS' and row[3] != '':
        proc = row[3]
    else:
        proc = row[2]

    # fix double entries -- need to check with the source!

    # fix multiple companies per row

    sname = row[4]

    newrow.extend([aid, ayear, amonth, aday, proc, sname, pesos, row[12], row[13], row[14], int(row[14])-int(row[13])])
    print newrow
    newdata.append(newrow)
    newrow = []

with open("outputfile.csv","w") as outputfile:
    writer = csv.writer(outputfile)
    header = ["award ID", "award year", "award month", "award day", "procedure", "original company name", "pesos", "ammendments", "contract begin", "contract end", "contract duration"]
    writer.writerow(header)

    writer.writerows(newdata)
    
            
           
