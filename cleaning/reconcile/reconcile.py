# -*- coding: utf-8 -*-

import csv, urllib, simplejson

def BestMatch(sname, api_code):

    url = "https://opencorporates.com/reconcile/?query="+urllib.quote(sname)
    entities = simplejson.load(urllib.urlopen(url))

    try:
        bm = entities['result'][0]
        url = "https://api.opencorporates.com" + bm['id'] + '?api_token='+ api_code

        match = simplejson.load(urllib.urlopen(url))
        m = match['results']['company']

        if m['controlling_entity'] == None:
            cen = ''
            cec = ''
            ceu = ''
        else:
            cen = m['controlling_entity']['name']
            cec = m['controlling_entity']['jurisdiction_code']
            ceu = m['controlling_entity']['opencorporates_url']
    

        print sname, m['name'], m['jurisdiction_code'], m['company_number'], m['corporate_groupings'], m['agent_name'], m['agent_address'], m['alternative_names'], m['previous_names'], m['home_company'], cen, cec, ceu, m['inactive'], bm['score'], bm['match'], bm['uri'], m['registry_url']
        reconciled.writerow([sname, m['name'].encode('utf-8'), m['jurisdiction_code'], m['company_number'], m['corporate_groupings'], m['agent_name'], m['agent_address'], m['alternative_names'], m['previous_names'], m['home_company'], cen, cec, ceu, m['inactive'], bm['score'], bm['match'], bm['uri'], m['registry_url']])
        
        return match['results']['company']['name']

    except IndexError:
        reconciled.writerow([sname, 'nomatch'])

        return "nomatch"

#input file
inputfile = open("../pemex.csv")
pemex = csv.reader(inputfile)

# my supersecret api_token
# get your own at https://opencorporates.com/api_accounts/new
api_token = open("api_token").read()

# already reconciled
inputfile = open("reconciled.csv")
done = [r[0] for r in csv.reader(inputfile)]
suppliers = []

# outputfile
with open("reconciled_output.csv", "w") as cnames:
    reconciled = csv.writer(cnames)
    rheader = ['original name', 'OC name', 'jurisdiction_code', 'company_number','corporate_groupings', 'agent_name', 'agent_address', 'alternative_names', 'previous_names', 'home_company', 'controlling_entity_name', 'controlling_entity_country', 'controlling_entity_oc_url', 'inactive','score','match','uri','registry_url']
    reconciled.writerow(rheader)


    pemex.next()
    for row in pemex:

        # reconcile API, example: http://onlinejournalismblog.com/tag/opencorporates/

        sname = row[4]

        # skip already reconciled
        if sname in suppliers or sname in done:
            print "done!"
            continue

        else:
            BestMatch(sname, api_token)
            suppliers.append(sname)
            print sname

    
            
           
