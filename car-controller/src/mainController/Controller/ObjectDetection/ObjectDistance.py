# @PascalPuchtler

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

import math

class ObjectDistance:
    def __init__(self, angleWidthCamera = 60* math.pi /180, correctionValuePyloneToDistance = 118253):
        self.angleWidthCamera = angleWidthCamera
        self.correctionValuePyloneToDistance = correctionValuePyloneToDistance

    def addDistance(self, pylons, imgColor, imgDeep):
        for pylone in pylons:
            middleX = int((pylone['xmax']+pylone['xmin'])/2)
            middleY = int((pylone['ymax']+pylone['ymin'])/2)
            pylone['distanceAbsolut'] = 0
            pylone['angle'] = self.getAngleX(imgColor,middleX)

            if imgDeep is not None:
                pylone['distanceAbsolut'] = self.getDeepFromDeepImage(imgDeep, middleX, middleY)/1000

            deltaY = pylone['ymax']-pylone['ymin']
            if pylone['distanceAbsolut'] == 0:
                callulatedDistance = self.getDistanceFromObjectDetection(deltaY)/1000
                if callulatedDistance < 2:
                    pylone['distanceAbsolut'] = callulatedDistance

            pylone['distanceX'] = pylone['distanceAbsolut']*math.sin(pylone['angle'])
            pylone['distanceY'] = pylone['distanceAbsolut']*math.cos(pylone['angle'])

    def getAngleX(self, imgColor, middleX):
        totalPixelX =imgColor.shape[1]
        #degrees form Object in x to camera
        pixelMiddelX = middleX-int(totalPixelX/2)
        radMiddel = pixelMiddelX/totalPixelX*self.angleWidthCamera
        return  radMiddel

    def getDistanceFromObjectDetection(self, deltaY):
        return self.correctionValuePyloneToDistance / deltaY

    def getDeepFromDeepImage(self,imgDeep, middleX, middleY):
        return imgDeep[middleY][middleX]
