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

import numpy as np
from scipy.spatial import distance


class MapPoint:

    def __init__(self, x = 0, y = 0, orientation = 0):
        self._x =x
        self._y =y
        self._orientation = orientation

    def getEndpoint(self, radius, distance):
        if radius == 0:
            return self.getEndpointRadiusZero(distance)
        return self.getEndpointNotZeroRadius(radius,distance)

    def getEndpointRadiusZero(self,distance):        
        R = self.getRotationMatrix(self.orientation)
        endPoint = R @ np.array([0,distance])
        endPoint = MapPoint(endPoint[0],endPoint[1],0)
        endPoint = endPoint + self
        return endPoint

    def getEndpointNotZeroRadius(self, radius, distance):
        angle = distance/radius
        y = math.sin(angle)*radius
        x = - math.cos(angle)*radius + radius
        
        R = self.getRotationMatrix(self.orientation)
        endPoint = R @ np.array([x,y])
        endPoint = MapPoint(endPoint[0],endPoint[1],angle)
        endPoint = endPoint + self
        return endPoint

    def getRelativeOffsetsToPoint(self,x, y):
        deltaX = x - self.x
        deltaY = y - self.y
        R = self.getRotationMatrix(-self.orientation)
        endPoint = R @ np.array([deltaX,deltaY])
        return endPoint

    def getRelativeAngleToPoint(self,x,y):
        endPoint = self.getRelativeOffsetsToPoint(x,y)
        angle = np.arctan2(endPoint[0],endPoint[1])
        return angle

    def getAbsolutPointFromRelativeOffset(self,x,y):
        R = self.getRotationMatrix(self.orientation)
        deltaPoint = R @ np.array([x,y])
        endPoint = deltaPoint + np.array([self.x, self.y])
        return endPoint

    def distance(self,x,y):
        return distance.euclidean((self.x,self.y),(x,y))


    def getRotationMatrix(self,angle):
        c, s = np.cos(-angle), np.sin(-angle)
        return np.array(((c, -s), (s, c)))


    def __str__(self):
        return 'Point x: ' + str( round(self.x,3)) + ' y: ' + str(round(self.y,3)) + ' orientation: ' + str(round(self.orientation,3))  

    def __eq__(self,other):
        if not np.isclose(self.x, other.x):
            return False
        
        if not np.isclose(self.y, other.y):
            return False
        
        if not np.isclose(math.sin(self.orientation), math.sin(other.orientation)) or not np.isclose(math.cos(self.orientation), math.cos(other.orientation)):
            return False
    
        return True

    def __add__(self,other):
        return MapPoint(self.x + other.x, self.y + other.y, self.orientation + other.orientation)
        
    def __sub__(self, other):
        return self + - other

    def __abs__(self):
        return distance.euclidean((self.x,self.y),(0,0))

    def __neg__(self):
        return MapPoint(- self.x, - self.y, - self.orientation)

    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @property
    def orientation(self):
        return self._orientation
