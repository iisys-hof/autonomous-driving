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

import math
import sys
import time

import numpy as np
from planar import Polygon

from Controller.AreaMap.MapPoint import MapPoint
from Controller.MoveController.CarModel import CarModel

from .NearestNeighbor import NearestNeighbor
from .SupportPointChain import SupportPointChain


class TrajectoryPlanning:
    
    def __init__(self, areaMap, emergencyStopQueue):
        self.areaMap = areaMap
        self.emergencyStopQueue = emergencyStopQueue
        self.carModel = CarModel()
        self.nearestNeighbor = NearestNeighbor()
        self.supportPointChain = SupportPointChain()
        self.reset()
        self.maxDriveableSlope = 3
        self.normalMode = True
        self.minImageCount = 6
        self.imageCount = 0

    def reset(self):
        self.newestSupportChain = []
        self.callculatedNextMove = None

    def nextMove(self):
        self.imageCount +=1
        if self.minImageCount > self.imageCount:
            self.callculatedNextMove = {'x': 0, 'y': 0, 'm': 0}
            return self.callculatedNextMove

        nextMove = self.handleNextMove()

        if not self.emergencyStopQueue.empty():
            print('emergeny mode')
            self.emergencyStopQueue.get()
            self.normalMode = False

        elif self.normalMode is False and nextMove is not None:
            self.normalMode = True
            print('reset Mode')
            return {'command': 'resetSavety'}

        if self.normalMode:
            if nextMove is not None:
                self.callculatedNextMove = nextMove
                return nextMove
            self.callculatedNextMove = {'x': 0, 'y': 0, 'm': 0}
            return {'x': 0, 'y': 0, 'm': 0}
        else:
            self.callculatedNextMove = {'x': 0, 'y': 0, 'm': 0}
            self.areaMap.reset()
            self.imageCount=0
            return {'x': 0, 'y': 0, 'm': 0}

    def handleNextMove(self):
        if not self.areaMap.isBorderAvailable():
            # print('no border available')
            return None
        supportPoints = self.nearestNeighbor.getNearestNeighbor(self.areaMap.left, self.areaMap.right)
        supportPointChain = self.supportPointChain.getSupportPointChain(supportPoints, self.areaMap.robotPosition)
        self.newestSupportChain = supportPointChain
        if len(supportPointChain)<=1:
            print('no possible target in drive direction')
            return None
        nextMove = self.callculateNextTarget(self.areaMap.robotPosition, supportPointChain)
        return nextMove


    def callculateNextTarget(self,robotPosition, supportPointChain):
        nextPoint = supportPointChain[1]

        offsetNextPoint = robotPosition.getRelativeOffsetsToPoint(nextPoint[0],nextPoint[1])
        
        if len(supportPointChain) >= 3:
            secondPoint = supportPointChain[2]
            offsetSecondPoint = robotPosition.getRelativeOffsetsToPoint(secondPoint[0],secondPoint[1])
            slope = self.slope(offsetNextPoint, offsetSecondPoint)
            if offsetNextPoint[1] < offsetSecondPoint[1]:
                slope = -slope

        else:
            slope = 0

        return {'x': offsetNextPoint[1], 'y': -offsetNextPoint[0], 'm': slope/2}


    def slope(self, point1, point2):
        m = (point2[0]-point1[0])/(point2[1]-point1[1])
        m= np.clip(m, -self.maxDriveableSlope,self.maxDriveableSlope)
        return m
