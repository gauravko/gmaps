import math
import json
import requests
from mercatorProjection import fromPointToLatLong, fromLatLongToPoint

EARTH_RADIUS = 6378137
MIN_LAT = -85.05112878
MAX_LAT = 85.05112878
MIN_LNG = -180
MAX_LNG = 180

def latRad(latitude):
    sin = math.sin( latitude * math.pi / 180 )
    radx2 = math.log((1+sin)/(1-sin))/2
    return max(min(radx2, math.pi), -math.pi)/2

def calcZoom(mapPx, worldPx, fraction):
    return round(math.log(mapPx / worldPx / fraction) / math.log1p(1))

def latRad(lat):
    sin = math.sin( lat * math.pi/180)
    radx2 = math.log( (1 + sin)/ (1 - sin))/2
    return max( min(radx2, math.pi), -math.pi)/2

def calcZoom(mapPx, worldPx, fraction):
    print(mapPx, worldPx, fraction)
    return math.floor(math.log( mapPx/worldPx/fraction)/ math.log1p(1))

def getBoundaries(bounds):

    northEast = { 'lat' : max(bounds, key=lambda x:x['lat'])['lat'], 'lng' : max(bounds, key=lambda x:x['lng'])['lng']}
    southWest = {'lat': min(bounds, key=lambda x: x['lat'])['lat'], 'lng': min(bounds, key=lambda x: x['lng'])['lng']}

    return northEast, southWest

def calcMapSize(zoom):
    return 256 << zoom

def clip(n, minValue, maxValue):
    return min(max(n, minValue), maxValue)

def LatLongttoPixel(latLng, zoom):
    lat = clip(latLng['lat'], MIN_LAT, MAX_LAT)
    lng = clip(latLng['lng'], MIN_LNG, MAX_LNG)

    x = (lng + 180)/360

    siny = math.sin(lat * math.pi/180)
    y = 0.5 - math.log( (1 + siny)/(1 - siny))/(4 * math.pi)

    mapSize = calcMapSize(zoom)

    pixelX = int()

def getBoundsZoomLevel(bounds, mapDim):
    WORLD_DIM = { 'height': 256, 'width': 256}
    ZOOM_MAX = 21

    '''northEast = getNorthEast(bounds)
    southWest = getSouthWest(bounds)'''

    northEast, southWest = getBoundaries(bounds)

    latFraction = (latRad(northEast['lat']) - latRad(southWest['lat']))/math.pi

    lngDiff = northEast['lng'] - southWest['lng']
    if lngDiff < 0:
        lngFraction = (lngDiff + 360)/360
    else:
        lngFraction = lngDiff/360

    latZoom = calcZoom(mapDim['height'], WORLD_DIM['height'], latFraction)
    lngZoom = calcZoom(mapDim['width'], WORLD_DIM['width'], lngFraction)


    return min(latZoom, lngZoom, ZOOM_MAX)

def calcBounds(point, zoom, width, height):

    scale = math.pow(2.0, float(zoom))

    centerPx = fromLatLongToPoint(point)

    southWestPoint = { 'x': centerPx['x'] - (width/2)/scale, 'y': centerPx['y'] + (height/2)/scale }
    southWestLatLng = fromPointToLatLong(southWestPoint)

    northEastPoint = { 'x': centerPx['x'] + (width/2)/scale, 'y': centerPx['y'] - (height/2)/scale }
    northEastLatLng = fromPointToLatLong(northEastPoint)

    return northEastLatLng, southWestLatLng


def getLatLngtoPixel(latLng, zoom):
    siny = math.sin(latLng['lat'] * math.pi / 180)
    pixelX = ((latLng['lng'] + 180) / 360) * 256 * math.pow(2, zoom)
    pixelY = (0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi)) * 256 * math.pow(2, zoom)
    return {'x': pixelX, 'y': pixelY }


def getCentre(bounds):
    centre = { 'lat': 0, 'lng': 0}

    for marker in bounds:
        centre['lat'] += marker['lat']
        centre['lng'] += marker['lng']

    centre['lat'] = centre['lat']/len(bounds)
    centre['lng'] = centre['lng']/len(bounds)

    print('centre is ', json.dumps(centre))
    return centre







