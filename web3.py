from io import BytesIO

from PIL import Image
import requests
import sys
from web_func import get_coords, find_distance_degrees_and_radians

search_api_server = "https://search-maps.yandex.ru/v1/"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
api_key_search = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
api_key_geocoder = "40d1649f-0493-4b70-98ba-98533de7710b"

toponym_to_find = " ".join(sys.argv[1:])

geocoder_params = {
    "apikey": api_key_geocoder,
    "geocode": toponym_to_find,
    "format": "json"}

tmp_response = requests.get(geocoder_api_server, params=geocoder_params)
result_tmp_response = tmp_response.json()
address_ll = get_coords(result_tmp_response)

search_params = {
    'apikey': api_key_search,
    'text': 'аптека',
    'lang': 'ru_RU',
    'll': address_ll,
    'type': 'biz'
}
response = requests.get(search_api_server, params=search_params)
if not response:
    pass

orgs_names = []
orgs_addresses = []
points = []
corgs_points = []
count = 10
no_inform = None
json_response = response.json()
organization = json_response["features"][:count]
pt_param = f'{address_ll},pm2vvl'
for i in range(0, count):
    orgs_names.append(organization[i]["properties"]["CompanyMetaData"]["name"])
    orgs_addresses.append(organization[i]["properties"]["CompanyMetaData"]["address"])
    point = organization[i]["geometry"]["coordinates"]
    cords = "{0},{1}".format(point[0], point[1])
    corgs_points.append(cords)
    corgs_points.append(cords)
    hours = organization[i]["properties"]["CompanyMetaData"]['Hours']['text']
    if not hours:
        color = 'gr'
    elif 'круглосуточно' in hours.split():
        color = 'gn'
    elif 'круглосуточно' not in hours.split():
        color = 'bl'
    pt_param += f'~{cords},pm2{color}l'


distance = find_distance_degrees_and_radians([corgs_points[-1], address_ll.split()[-1]])


delta = distance
map_params = {
    "ll": address_ll,
    "spn": ",".join([str(delta[5] + 0.005), str(delta[4] + 0.005)]),
    "l": "map",
    "pt": pt_param
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
