import requests, json, urllib, cStringIO
from StringIO import StringIO
from mapEngine import getBoundsZoomLevel, getCentre, calcBounds, getLatLngtoPixel
from mercatorProjection import fromPointToLatLong, fromLatLongToPoint
from PIL import Image, ImageDraw

FLICKR_RANDOM_IMAGE_URL = 'http://lorempixel.com//80/60'
_workingDirectory = 'temp/'

def generateMap(markers, mapDim):

    zoom = getBoundsZoomLevel(markers, mapDim)

    marker_args = '&markers='
    firstMarker = True
    for marker in markers:
        if not firstMarker:
            marker_args += '|'
        marker_args += str(marker['lat']) + ',' + str(marker['lng'])
        firstMarker = False

    staticMapUrl = ''.join([
        'http://maps.googleapis.com/maps/api/staticmap',
        '?style=feature:all|element:all|saturation:-80|gamma:0.4&sensor=false&v=3&visual_refresh=true',
        '&size={}x{}&zoom={}'.format(
            mapDim['width'], mapDim['height'], zoom),
        marker_args,])

    print(staticMapUrl)

    r = requests.get(staticMapUrl)
    file = open(_workingDirectory + 'test.png', 'wb+')
    file.write(r.content)
    file.close()

    return zoom
'''
def generateCompositeImage(markers, mapDim, zoom):
    centreLatLng = getCentre(markers)

    staticMapIm = Image.open(_workingDirectory + 'test.png')
    newImage = staticMapIm.copy()
    newImage.convert('RGBA')

    #Using Flick random image generator
    r = requests.get(FLICKR_RANDOM_IMAGE_URL)
    file = open(_workingDirectory + 'tempflick.png', 'wb+')
    file.write(r.content)
    file.close()


    tempPic = Image.open(_workingDirectory + 'natalie.jpg')
    tempPic.convert('RGBA')
    thumbnail = tempPic.resize((80,60), Image.ANTIALIAS)

    centrePx = getLatLngtoPixel(centreLatLng, zoom)

    NorthWestPx = { 'x': centrePx['x'] - mapDim['width']/2, 'y': centrePx['y'] - mapDim['height']/2}

    for marker in markers:
        markerPx = getLatLngtoPixel(marker, zoom)

        x_coordinate = int((markerPx['x'] - NorthWestPx['x']))
        y_coordinate = int(markerPx['y'] - NorthWestPx['y'])

        print(x_coordinate, y_coordinate)
        newImage.paste(thumbnail, (x_coordinate, y_coordinate))

    newImage.save(_workingDirectory + 'result.png')
'''

def getPixelsFromMarkers(markers, zoom):
    centreLatLng = getCentre(markers)
    centrePixelXY = getLatLngtoPixel(centreLatLng, zoom)

    pixelsXY = []

    for marker in markers:
        pixelsXY.append(getLatLngtoPixel(marker, zoom))

    return centrePixelXY, pixelsXY


def genCompositeImage(centrePixelXY, pixelsXY, zoom, mapDim):

    northWestPixelXY = { 'x': centrePixelXY['x'] - mapDim['width']/2, 'y': centrePixelXY['y'] - mapDim['height']/2}

    staticMapIm = Image.open(_workingDirectory + 'test.png')
    newImage = staticMapIm.copy()

    tempPic = Image.open(_workingDirectory + 'natalie.jpg')
    tempPic.convert('RGBA')
    thumbnail = tempPic.resize((80, 60), Image.ANTIALIAS)

    for pixel in pixelsXY:
        x_coordinate = int( pixel['x'] - northWestPixelXY['x'] ) - 40
        y_coordinate = int( pixel['y'] - northWestPixelXY['y'] ) - 30

        print(x_coordinate, y_coordinate)
        newImage.paste(thumbnail, (x_coordinate, y_coordinate))

    newImage.save(_workingDirectory + 'result.png')


def generateCompositeImage(markers, mapDim, zoom, northWest, northEast, southWest):
    northWestPoint = fromLatLongToPoint(northWest)
    northEastPoint = fromLatLongToPoint(northEast)
    southWestPoint = fromLatLongToPoint(southWest)

    staticMapIm = Image.open(_workingDirectory + 'test.png')
    newImage = staticMapIm.copy()

    r = requests.get(FLICKR_RANDOM_IMAGE_URL)
    file = open(_workingDirectory + 'tempflick.png', 'wb+')
    file.write(r.content)
    file.close()

    tempPic = Image.open(_workingDirectory + 'natalie.jpg')
    tempPic.convert('RGBA')
    thumbnail = tempPic.resize((80, 60), Image.ANTIALIAS)

    for marker in markers:
        markerPoint = fromLatLongToPoint(marker)

        x_coordinate = int( (markerPoint['x'] - northWestPoint['x'])*mapDim['width']/(northEastPoint['x'] - northWestPoint['x']) )
        y_coordinate = int(
            (markerPoint['y'] - northWestPoint['y']) * mapDim['height'] / (southWestPoint['y'] - northWestPoint['y']))

        print(x_coordinate, y_coordinate)
        newImage.paste(thumbnail, (x_coordinate, y_coordinate))

    newImage.save(_workingDirectory + 'result.png')

def main():
    markers = [
    { 'lat': 12.907559, 'lng': 77.636497},
    { 'lat': 12.909561, 'lng': 77.632420},
    { 'lat': 12.908742, 'lng': 77.634882}
    ]

    mapDim = {'height': 480, 'width': 640}

    zoom, northWest, northEast, southWest = generateMap(markers, mapDim)

    #generateCompositeImage(markers, mapDim, zoom, northWest, northEast, southWest)

    centrePixel, pixels = getPixelsFromMarkers(markers, zoom)
    genCompositeImage(centrePixel, pixels, zoom, mapDim)

if __name__ == '__main__':
    main()

'''
Istanbul co-ordinates

    markers = [
        {'lat': 41.007880, 'lng': 28.982449},
        {'lat': 41.006959, 'lng': 29.011974},
        {'lat': 41.037330, 'lng': 28.984423}
    ]

London

    markers = [
        {'lat': 51.527085, 'lng': -0.132952},
        {'lat': 51.512665, 'lng': -0.070810},
        {'lat': 51.501981, 'lng': -0.103083},
        {'lat': 51.505507, 'lng': -0.189772}
    ]

London, New Delhi

    markers = [
        {'lat': 51.527085, 'lng': -0.132952},
        {'lat': 28.613939, 'lng': 77.209021}

    ]

Delhi, Kolkata, Mumbai, Bangalore, Ceylon

    markers = [
        { 'lat' : 28.704059, 'lng' : 77.102490},
        { 'lat' : 22.572646, 'lng' : 88.363895},
        { 'lat' : 19.075984, 'lng' : 72.877656},
        { 'lat' : 12.971599, 'lng' : 77.594563},
        { 'lat' : 7.873054,  'lng' : 80.771797}
    ]

HSR Layout

    markers = [
    { 'lat': 12.907559, 'lng': 77.636497},
    { 'lat': 12.909561, 'lng': 77.632420},
    { 'lat': 12.908742, 'lng': 77.634882}
    ]
'''