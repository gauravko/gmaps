import math
import json
import requests
from mercatorProjection import fromPointToLatLong, fromLatLongToPoint

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
    return math.floor(math.log( mapPx/worldPx/fraction)/ math.log1p(1))

def getNorthEast(bounds):
    northEast = bounds[0]

    for marker in bounds:
        if marker['lat'] > northEast['lat']:
            northEast['lat'] = marker['lat']
        if marker['lng'] > northEast['lng']:
            northEast['lng'] = marker['lng']

    return northEast

def getSouthWest(bounds):
    southWest = bounds[0]

    for marker in bounds:
        if marker['lat'] < southWest['lat']:
            southWest['lat'] = marker['lat']
        if marker['lng'] < southWest['lng']:
            southWest['lng'] = marker['lng']

    return southWest

def getBoundsZoomLevel(bounds, mapDim):
    WORLD_DIM = { 'height': 256, 'width': 256}
    ZOOM_MAX = 21

    northEast = getNorthEast(bounds)
    southWest = getSouthWest(bounds)

    northEast = {"lat": 41.03733, "lng": 29.011974}

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

    centerPx = fromLatLongToPoint({ 'lat': point['lat'], 'lng': point['lng']})

    southWestPoint = { 'x': centerPx['x'] - (width/2)/scale, 'y': centerPx['y'] + (height/2)/scale }
    southWestLatLng = fromPointToLatLong(southWestPoint)

    northEastPoint = { 'x': centerPx['x'] + (width/2)/scale, 'y': centerPx['y'] - (height/2)/scale }
    northEastLatLng = fromPointToLatLong(northEastPoint)

    return northEastLatLng, southWestLatLng

def getCentre(bounds):
    count = 0
    centre = { 'lat': 0, 'lng': 0}

    for marker in bounds:
        count += 1
        centre['lat'] += marker['lat']
        centre['lng'] += marker['lng']

    centre['lat'] = centre['lat']/count
    centre['lng'] = centre['lng']/count

    return centre







