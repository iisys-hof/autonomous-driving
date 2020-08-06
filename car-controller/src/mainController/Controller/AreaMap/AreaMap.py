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
import operator
import time

import numpy as np

from Controller.AreaMap.MapPoint import MapPoint
from Controller.EkfSlam.EkfSlam import EKFSlam
class AreaMap:

    def __init__(self, realMovementQuees, angleWidthCammera):
        self.ekfSlam = EKFSlam()
        self.reset()
        self.realMovementQuees = realMovementQuees
        self.minDistanceRobotPositionHistory = 0.1
        self.angleWidthCammera = angleWidthCammera*0.9
        self.maxTimeSinceLastViewed = 25

    def reset(self):
        self.ekfSlam.reset()
        
        self.robotPosition = MapPoint(0,0,0)
        self.landMarks =[]

        self.left = []
        self.right = []
        self.others = []
        self.lastTime =  time.time()
        self.lastGear = 0
        self.lastSpeed = 0

        self.robotPositionsHistory = [self.robotPosition]

    def updatePylons(self, pylons):
        pylons = [pyl for pyl in pylons if pyl['distanceAbsolut'] >0]
        observaitons = np.array([[obj['distanceAbsolut'], obj['angle']] for obj in pylons])

        robotPositonUpdate = self.callculateGearAndSpeed()

        self.ekfSlam.update(robotPositonUpdate, observaitons)
        robotPosition = self.ekfSlam.getRobotPosition()
        positionLandMarks = self.ekfSlam.getLandmarkPositions()
        observationIDS = self.ekfSlam.getOberservationIDs()
        

        self.updateLandmarks(positionLandMarks, pylons, observationIDS)
        self.updateLandmarkIsVisible(observationIDS)

        self.robotPosition = MapPoint(robotPosition[1], robotPosition[0], robotPosition[2])
        self.updateLandmarkSchouldVisible()

        self.addPositionHistory()

        self.deleteLandmarks()

        self.left = self.getBorder('b')
        self.right = self.getBorder('y')
        self.others = self.getBorder('o')
        
    def updateLandmarks(self, positionLandMarks, pylons, observationIDS):
        lastViewed = time.time()
        for i in range(positionLandMarks.shape[0]):
            if i >= len(self.landMarks):
                self.landMarks.append({
                    'label':{},
                    'negativCount': 0
                })
            lm = self.landMarks[i]
            pos = positionLandMarks[i]
            lm['x'] = pos[1]
            lm['y'] = pos[0]

            if i in observationIDS:
                pylone = pylons[observationIDS.index(i)]
                if pylone['label'] not in lm['label']:
                    lm['label'][pylone['label']] = 0    
                lm['label'][pylone['label']] +=1
                lm['mayorLabel'] = max(lm['label'].items(), key=operator.itemgetter(1))[0]
                lm['lastViewed'] = lastViewed
            
    
    def updateLandmarkIsVisible(self, observationIDS):
        for i, landmark in enumerate(self.landMarks):
            if i in observationIDS:
                landmark['isVisible'] = True
            else:
                landmark['isVisible'] = False

    def updateLandmarkSchouldVisible(self):
        for landmark in self.landMarks:
            angle = self.robotPosition.getRelativeAngleToPoint(landmark['x'], landmark['y'])
            if -self.angleWidthCammera/2 <= angle <= self.angleWidthCammera/2:
                landmark['shouldVisible'] = True
            else:
                landmark['shouldVisible'] = False

    def deleteLandmarks(self):
        lmToDelete  = [index for index, lm in enumerate(self.landMarks) if self.isLandmarkToDelete(lm)]
        lmToDelete.reverse()
        for i in lmToDelete:
            lm = self.landMarks[i]
            self.ekfSlam.deleteLandmarkID(i)
            self.landMarks.remove(lm)

    def isLandmarkToDelete(self,lm):
        lastViewd = time.time() - lm['lastViewed']
        return self.maxTimeSinceLastViewed < lastViewd


    def getBorder(self,label):
        targetBorder=[lm for lm in self.landMarks if lm['mayorLabel'] == label and lm['label'][label]>1]
        return targetBorder

    def callculateGearAndSpeed(self ):
        gear =0
        speed = 0
        actualTime = time.time()
        lastTime = self.lastTime
        lastGear = self.lastGear
        lastSpeed = self.lastSpeed

        while not self.realMovementQuees.empty():
            movementCommand = self.realMovementQuees.get()
            deltaTime = movementCommand['time'] - lastTime
            gear+=lastGear*deltaTime
            speed+=lastSpeed*deltaTime
            lastGear =  movementCommand['gear'] 
            lastTime =  movementCommand['time'] 
            lastSpeed =  movementCommand['speed'] 

        deltaTime =actualTime-  lastTime
        gear+=lastGear*deltaTime
        speed+=lastSpeed*deltaTime

        self.lastGear = lastGear
        self.lastSpeed = lastSpeed
        self.lastTime = actualTime
        robotPositonUpdate = np.array([[speed, gear]]).T
        return robotPositonUpdate

    def addPositionHistory(self):
        if abs(self.robotPosition-self.robotPositionsHistory[-1]) > self.minDistanceRobotPositionHistory:
            self.robotPositionsHistory.append(self.robotPosition)

    def getNearestLeft(self):
        pos = np.argmin([pos[1] for pos in self.left])
        return self.left[pos]
    
    def getNearestRight(self):
        pos = np.argmin([pos[1] for pos in self.right])
        return self.right[pos]

    def isBorderAvailable(self):
        return len(self.left)>0 and len(self.right)>0

