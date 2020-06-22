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

import time

import numpy as np
from scipy.interpolate import CubicHermiteSpline as Spline

class DriveCurve:
    
    def __init__(self, carModel):
        self.carModel = carModel
        self.reset()

    def reset(self):
        self.lastTime =  time.time()
        self.position = 0
        self.radius = 0
        self.maxPosition =0

    def setCurve(self, curve):
        if curve['x']>0:
            print(curve)
            self.reset()
            self.spline = Spline([0,curve['x']], [0,curve['y']], [0,curve['m']])
            self.maxPosition = curve['x']
        

    def getNextRadius(self):
        actualTime = time.time()
        deltaTime = actualTime - self.lastTime
        speed = self.carModel.getMotorSpeedFromRadius(self.radius, True, True)[2]
        self.position += deltaTime* speed * np.cos(np.arctan(self.spline(self.position,1)))

        self.radius = self.getRadiusFromDistance(self.position)
        self.lastTime = actualTime
        print('')
        print(round(self.position/self.maxPosition*100), '%', round(self.radius,4) ,'m')
        return self.radius

    def isDriving(self):
        return self.maxPosition * 0.2 > self.position

    def getRadiusFromDistance(self,x):
        fx1 = self.spline(x,1)
        fx2 = self.spline(x,2)

        if np.isclose(0,fx2):
            return float("inf")
        radius = ((1 + fx1*fx1)**(3/2))/ fx2
        return -radius

    def lengthOfSpline(self, spline, start, stop, steps=100):
        supportPoints = np.linspace(start, stop, steps)
        points = spline(supportPoints)
        points = np.array([supportPoints,points])
        print(points)
        length =np.sum( np.sqrt(np.sum(np.diff(points, axis=1)**2, axis=0)))
        print(length)
        return length
