import math


def make_appropriate_scale(result_tmp_response):
    size_information = result_tmp_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]['boundedBy']
    low_corner = size_information['Envelope']['lowerCorner'].split()
    upper_corner = size_information['Envelope']['upperCorner'].split()
    x_size = float(upper_corner[0]) - float(low_corner[0])
    y_size = float(upper_corner[1]) - float(low_corner[1])
    return f'{x_size},{y_size}'


def get_coords(tmp_toponym):
    toponym = tmp_toponym["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    return ','.join(toponym_coodrinates.split())


def find_distance(coords):
    coords1, coords2 = (i.replace(',', ' ').split() for i in coords)
    lat1, lon1 = map(lambda x: float(x), coords1)
    lat2, lon2 = map(lambda x: float(x), coords2)
    radius = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance
