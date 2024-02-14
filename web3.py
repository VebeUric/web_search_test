from io import BytesIO

from PIL import Image
import requests
import sys
from web_func import get_coords, find_distance

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


# Преобразуем ответ в json-объект
json_response = response.json()
organization = json_response["features"][0]

org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
print()

point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
delta = "0.005"
coordss = [org_point, address_ll]
print(coordss[1])
map_params = {
    "ll": address_ll,
    "spn": ",".join([delta, delta]),
    "l": "map",
    "pt": "{0},pm2dgl~{1},pm2rdl".format(*coordss)
}

organization_info = organization["properties"]["CompanyMetaData"]
# organization_snipet = {'working_time': organization_info['Hours'],
#                        'phone_number': organization_info[]
distance = find_distance(coordss)
organization_snipet = f" Название: {org_name} \n Адресс: {org_address} Часы работы: {organization_info['Hours']} \n " \
                      f"Номер телефона: {organization_info['Phones'][0]['formatted']} \n Расстояние до места: {distance if distance > 1 else distance * 1000} "
print(organization_snipet)


map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
