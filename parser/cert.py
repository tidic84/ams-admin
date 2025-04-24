import requests
from bs4 import BeautifulSoup
import json

response = requests.get('https://www.cert.ssi.gouv.fr/')
soup = BeautifulSoup ( response.content , "html.parser" )
cert = soup.find_all('div', class_='item cert-alert open')[0].find_all('div') 

result = {
    'date': cert[0].span.text.replace('  ','').replace('\n',''),
    'id': cert[1].a.text.replace('  ','').replace('\n',''),
    'title': cert[2].a.text.replace('  ','').replace('\n',''),
    'status': cert[3].span.text.replace('  ','').replace('\n','')
}

print(json.dumps(result))