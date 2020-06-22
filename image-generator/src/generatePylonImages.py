# Copyright 2020 @PascalPuchtler

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import cv2
import numpy as np
import random
from pascal_voc_writer import Writer

from ImageChangeColor import ImageChangeColor
from ImageLoader import ImageLoader
from PyloneLoader import PyloneLoader
from BackgroundLoader import BackgroundLoader
from ImageTransformation import ImageTransformation
from ImageNoise import ImageNoise

maximalPylonsPerImage = 11
numberImagesToCreate = 2000
numberTestImagesToCreate =200

basePath = 'D:/Projekte/autonomous-driving/'
savePath = basePath + 'working/images/'
saveTestPath = basePath + 'working/imagesTest/'

backGroundPath = basePath + 'pylon-images/background/'
pylonsPaths = [
     {
         'path':basePath + 'pylon-images/snippedGreenscreen/blue/',
         'label': 'blue'
    },
     {
         'path':basePath + 'pylon-images/snippedGreenscreen/orange/',
         'label': 'orange'
    },
     {
         'path':basePath + 'pylon-images/snippedGreenscreen/yellow/',
         'label': 'yellow'
}
]

imageChangeColor = ImageChangeColor()
pyloneLoader = PyloneLoader(pylonsPaths)
backgroundLoader = BackgroundLoader(backGroundPath)
imageTransformation = ImageTransformation()
imageNoise = ImageNoise()

def main():
    print('count images:', numberImagesToCreate)
    print('count test images:', numberTestImagesToCreate)
    print('maximalPylonsPerImage:', maximalPylonsPerImage)
    print(backgroundLoader)
    print(pyloneLoader)
    generateAndSaveImages(savePath, numberImagesToCreate)
    generateAndSaveImages(saveTestPath, numberTestImagesToCreate)
    print('ready')
        

def generateAndSaveImages(savePath, count):
    for count in range(count):
        pathWithFilename = savePath + 'image' + str(count)
        generateAndSaveOneImage(pathWithFilename)

def generateAndSaveOneImage(pathWithFilename):
        pylonCount = np.random.randint(0,maximalPylonsPerImage )
        image, infos = generateOneImage(generateDistances(pylonCount))
        xml = generateXML(infos, pathWithFilename+ '.png')
        cv2.imwrite(pathWithFilename + '.png',image)
        xml.save(pathWithFilename + '.xml')
        print('.',end='', flush=True)


def generateOneImage(distances):
    background = backgroundLoader.getRandomBackground()
    infos = []
    for distance in distances:
        info = getCorruptPylone( distance)
        background, info = addPyloneToBackground(background, info)
        infos.append(info)
    background = imageChangeColor.changeBrightness(background)
    background = imageChangeColor.changeGamma(background)
    background = imageNoise.addNoise(background)
    return background, infos

def getCorruptPylone(distance):
    pylon, label = pyloneLoader.getRandomPylon()
    pylon = imageTransformation.scale(pylon)
    pylon = imageTransformation.resizeImage(pylon, distance)
    size = pylon.shape[:2]
    pylon = imageTransformation.getRandomRotatedImage(pylon)

    mask = imageTransformation.getMaskFromGreenscreen(pylon)
    pylon = imageChangeColor.changeColor(pylon)
    pylon = imageChangeColor.changeGamma(pylon)

    info = {
        'distance': distance,
        'label': label,
        'size': size,
        'image': pylon,
        'mask': mask
    }
    return info

def generateXML(infos, path):
    xml = Writer(path, 640, 480)
    for info in infos:
        xml.addObject(info['label'], info['position'][1], info['position'][0], info['position'][1]+info['size'][1], info['position'][0]+info['size'][0])
    return xml

def addPyloneToBackground(background, infoPylone):
    position = getRandomPosition(background, infoPylone['size'])
    infoPylone['position'] = position
    background = overlayImage(background,infoPylone['image'],infoPylone['mask'], position[0], position[1])
    return background, infoPylone

def overlayImage(background, foreground, foregroundmask, posy=0, posx=0):
    fg = foreground.astype(float)
    bg = background.astype(float)
    mask = foregroundmask.astype(float) / 255

    dims = fg.shape
    bg_part = bg[posy:posy+dims[0], posx:posx+dims[1]]
    # print('Bg:{}, Mask:{}, Fg:{}'.format(background.shape,mask.shape,fg.shape))
    bg_part = cv2.multiply(bg_part, 1-mask)
    fg = cv2.multiply(fg, mask)
    bg_part = cv2.add(fg, bg_part)
    bg[posy:posy+dims[0], posx:posx+dims[1]] = bg_part
    return bg.astype(np.uint8)

def getRandomPosition(background, pylonSize):
    sizeBackground = background.shape[:2]
    x = np.random.randint(0,sizeBackground[0]-pylonSize[0])
    y = np.random.randint(0,sizeBackground[1]-pylonSize[1])
    return x,y

def generateDistances(count):
    distances = [random.uniform(0.1, 0.7) for x in range(count)]
    distancesSorted = np.sort(distances)
    return distancesSorted

if  __name__ == '__main__':
    main()

