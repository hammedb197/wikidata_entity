from urllib.request import urlopen
from urllib.parse import urlencode
import pandas as pd
import requests
import json

def getJSON(entity_name):
    params = urlencode({
        'format': 'json',
        'action': 'opensearch',
        'search': entity_name})
    API = "https://en.wikipedia.org/w/api.php"
    response = urlopen(API + "?" + params)
    return response.read().decode('utf-8')




def getDetails(entity_name):
    name = json.loads(getJSON(entity_name))[3][0]
    sparql_query = """
            prefix schema: <http://schema.org/>
            SELECT ?itemLabel ?occupationLabel ?genderLabel ?bdayLabel  ?countryofcitizenshipLabel ?familynameLabel ?motherLabel ?fatherLabel ?spouseLabel ?childLabel ?employerLabel ?positionheldLabel
            ?memberofLabel ?educatedatLabel ?academicdegreeLabel ?residenceLabel ?memberofpoliticalpartyLabel ?ethnicgroupLabel ?religionLabel ?militaryrankLabel
            WHERE {
                <%s> schema:about ?item .
               OPTIONAL { ?item wdt:P106 ?occupation . }
               OPTIONAL { ?item wdt:P21 ?gender . }
               OPTIONAL { ?item wdt:P569 ?bday . }
               OPTIONAL { ?item wdt:P27 ?countryofcitizenship . }
               OPTIONAL { ?item wdt:P734 ?familyname . }
               OPTIONAL { ?item wdt:P25 ?mother . }
               OPTIONAL { ?item wdt:P22 ?father . }
               OPTIONAL { ?item wdt:P26 ?spouse . }
               OPTIONAL { ?item wdt:P40 ?child . }
               OPTIONAL { ?item wdt:P108 ?employer . }
               OPTIONAL { ?item wdt:P39 ?positionheld . }
               OPTIONAL { ?item wdt:P463 ?memberof . }
               OPTIONAL { ?item wdt:P69 ?educatedat . }
               OPTIONAL { ?item wdt:P512 ?academicdegree . }
               OPTIONAL { ?item wdt:P551 ?residence . }
               OPTIONAL { ?item wdt:P102 ?memberofpoliticalparty . }
               OPTIONAL { ?item wdt:P172 ?ethnicgroup . }
               OPTIONAL { ?item wdt:P140 ?religion . }
               OPTIONAL { ?item wdt:P410 ?militaryrank . }


                SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
            }
        """ %name
    url = 'https://query.wikidata.org/sparql'

    r = requests.get(url, params={'format': 'json', 'query': sparql_query})
    data = r.json()


    entity_info = []
    for i in range(len(data['results']['bindings'])):
        keys_list = list(data['results']['bindings'][i])
        entity_dict = {}
        for j in keys_list:
            data['results']['bindings'][i][j]['value']
            entity_dict.update({
                j: data['results']['bindings'][i][j]['value']
            })
        entity_info.append(entity_dict)

    data_ = pd.DataFrame(entity_info)
    return data_.to_csv(entity_name + '.csv', index=False)




getDetails('Barack Obama')
