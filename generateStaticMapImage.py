import requests, json, urllib, cStringIO
from StringIO import StringIO
from mapEngine import getBoundsZoomLevel, getCentre, calcBounds, getLatLngtoPixel
from mercatorProjection import fromPointToLatLong, fromLatLongToPoint
from PIL import Image, ImageDraw

FLICKR_RANDOM_IMAGE_URL = 'http://lorempixel.com//80/60'
_workingDirectory = 'temp/'

def generateMap(markers, mapDim):

    zoom = getBoundsZoomLevel(markers, mapDim)

    marker_args = '&visible='
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


def generateCompositeImage(markers, mapDim, zoom):
    centreLatLng = getCentre(markers)

    staticMapIm = Image.open(_workingDirectory + 'test.png')
    newImage = staticMapIm.copy()

    #Using Flick random image generator
    r = requests.get(FLICKR_RANDOM_IMAGE_URL)
    thumbnail = Image.open(StringIO(r.content))
    thumbnail.save(_workingDirectory + 'tempflick.png')

    centrePx = getLatLngtoPixel(centreLatLng, zoom)

    NorthWestPx = { 'x': centrePx['x'] - mapDim['width']/2, 'y': centrePx['y'] - mapDim['height']/2}

    for marker in markers:
        markerPx = getLatLngtoPixel(marker, zoom)

        x_coordinate = int((markerPx['x'] - NorthWestPx['x']))
        y_coordinate = int(markerPx['y'] - NorthWestPx['y'])

        print(x_coordinate, y_coordinate)
        newImage.paste(thumbnail, (x_coordinate, y_coordinate))

    newImage.save(_workingDirectory + 'result.png')

def main():

    markers = [
        {'lat': 51.527085, 'lng': -0.132952},
        {'lat': 51.512665, 'lng': -0.070810},
        {'lat': 51.501981, 'lng': -0.103083},
        {'lat': 51.505507, 'lng': -0.189772}
    ]


    mapDim = {'height': 480, 'width': 640}

    zoom = generateMap(markers, mapDim)

    generateCompositeImage(markers, mapDim, zoom)


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
'''