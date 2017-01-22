import math

TILE_SIZE = 256.0
_pixelOrigin = {'x' : TILE_SIZE/2 , 'y' : TILE_SIZE/2}
_pixelsPerLonDegree = float(TILE_SIZE/360)
_pixelsPerLonRadian = float(TILE_SIZE / (2 * math.pi))

def getBound(value, optMin, optMax):
    if optMin != None:
        value = max(value, optMin)
    if optMax != None:
        value = min(value, optMax)
    return value

def fromLatLongToPoint(latLng):
    point = { 'x'  : None, 'y' : None}
    origin = _pixelOrigin

    point['x'] = origin['x'] + latLng['lng'] * _pixelsPerLonDegree

    siny = getBound(math.sin(math.radians(latLng['lat'])), -0.9999, 0.9999)
    point['y'] = origin['y'] + 0.5 * math.log( (1 + siny ) / (1 - siny))*(-_pixelsPerLonRadian)

    return point

def fromPointToLatLong(point):
    origin = _pixelOrigin
    lng = (point['x'] - origin['x'])/_pixelsPerLonDegree

    latRadians = (point['y'] - origin['y'])/(-_pixelsPerLonRadian)
    lat = math.degrees(2 * math.atan(math.exp(latRadians)) - math.pi/2)

    return {'lat' : lat, 'lng' : lng}


