import requests
from getZoomFromBounds import getBoundsZoomLevel, getCentre, calcBounds
from mercatorProjection import fromPointToLatLong, fromLatLongToPoint
from PIL import Image, ImageDraw

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
            mapDim['height'], mapDim['width'], zoom),
        marker_args,])

    print(staticMapUrl)

    r = requests.get(staticMapUrl)
    file = open(_workingDirectory + 'test.png', 'wb+')
    file.write(r.content)
    file.close()

    centreLatLng = getCentre(markers)

    northEast, southWest = calcBounds( centreLatLng, zoom, mapDim['height'], mapDim['width'])

    return northEast, southWest

def generateCompositeImage(markers, northEast, southWest, mapDim):
    northEastPoint = fromLatLongToPoint(northEast)
    southWestPoint = fromLatLongToPoint(southWest)

    staticMapIm = Image.open(_workingDirectory + 'test.png')
    newImage = staticMapIm.copy()
    thumbnail = Image.open(_workingDirectory + 'thumbnail.png')


    for marker in markers:
        markerPoint = fromLatLongToPoint(marker)
        x_coordinate = int( mapDim['height'] + ((markerPoint['x'] - northEastPoint['x'])*mapDim['height'])/(northEastPoint['x'] - southWestPoint['x']))
        y_coordinate = int(-((markerPoint['y'] - northEastPoint['y'])*mapDim['width'])/(northEastPoint['y'] - southWestPoint['y']))

        print(x_coordinate, y_coordinate)
        newImage.paste(thumbnail, (x_coordinate, y_coordinate))

    newImage.save(_workingDirectory + 'result.png')

def main():

    markers = [
        {'lat': 41.007880, 'lng': 28.982449},
        {'lat': 41.006959, 'lng': 29.011974},
        {'lat': 41.037330, 'lng': 28.984423}
    ]

    mapDim = {'height': 640, 'width': 480}

    northEast, southWest = generateMap(markers, mapDim)

    generateCompositeImage(markers, northEast, southWest, mapDim)



if __name__ == '__main__':
    main()

'''
Istanbul co-ordinates

    markers = [
        {'lat': 41.007880, 'lng': 28.982449},
        {'lat': 41.006959, 'lng': 29.011974},
        {'lat': 41.037330, 'lng': 28.984423}
    ]
'''