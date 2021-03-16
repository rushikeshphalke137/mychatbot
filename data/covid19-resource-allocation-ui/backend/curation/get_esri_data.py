import requests
import json
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--output', dest='outputname',required=False,default="covid_cases_esri")
parser.add_argument('--url', dest='url', required=False,default='https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=Confirmed+%3E+0&outFields=*&orderByFields=Confirmed%20desc')
args = parser.parse_args();

res = requests.get(args.url)

content = json.loads(res.content)
out=[]
out.append("name,Region,Last Update,Confirmed,Deaths,Recovered")
for data in content['features']:
  di = int(data['attributes']['Last_Update']) / 1000
  d = datetime.datetime.utcfromtimestamp(di).strftime("%Y-%m-%d %H:%M:%S") 
  out.append(f"{data['attributes']['Province_State']},{data['attributes']['Country_Region']},{d},{data['attributes']['Confirmed']},{data['attributes']['Deaths']},{data['attributes']['Recovered']}")

timeStamp = datetime.datetime.now().strftime('%H%M-%m%d%Y')
fileName = f'{args.outputname}-{timeStamp}'
print(f"Output {fileName}")

with open(fileName + '.json','w') as f:
  f.write(json.dumps(content))

with open(fileName + '.csv','w') as f:
  f.write('\n'.join(out))





