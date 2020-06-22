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

import numpy as np
from scipy.interpolate import interp1d

modelDataDiameter= np.array([384, 272, 234, 206, 132,110, 96, 85, 78 ,73])/100
modelDataSpeedOuterWheel =  np.array([30, 35, 40, 45, 50 ,60 ,70 , 80 , 90 ,100])
modelDataTime = np.array([76.8, 50.8, 36.4, 26.8, 18.4 , 13.5, 10.5 , 8.4 , 7.1 ,6.4])
modelDataSpeedInnerWheel = 20

modelDataDiameterBigRadius= np.array([88464, 2490, 1576, 1380, 1092, 768, 526, 480, 434])/100
modelDataSpeedInnerWheelBigRadius =  np.array([29, 28, 27, 26, 25, 24, 23, 22, 21])
modelDataTimeBigRadius = np.array([1186, 357, 228, 207, 173, 124, 80, 80, 80])
modelDataSpeedOutherWheel = 30


driveForwardConstantSpeed = 30

class CarModel:
    def __init__(self, widthCar = 0.28):
        self.widthCar = widthCar
        self.modelRadiusToCmdSpeed = interp1d(modelDataDiameter/2, modelDataSpeedOuterWheel, fill_value='extrapolate')
        self.modelRadiusToCarSpeed = interp1d(modelDataDiameter/2, (modelDataDiameter+widthCar/2)*np.pi/modelDataTime, fill_value='extrapolate')
        self.modelRadiusToCmdSpeedBigRadius = interp1d(modelDataDiameterBigRadius/2, modelDataSpeedInnerWheelBigRadius, fill_value='extrapolate')
        self.modelRadiusToCarSpeedBigRadius = interp1d(modelDataDiameterBigRadius/2, (modelDataDiameterBigRadius-widthCar/2)*np.pi/modelDataTimeBigRadius, fill_value='extrapolate')
        self.radiusSplitValue = (modelDataDiameterBigRadius[-1] +modelDataDiameter[0])/4
        self.maxRadius = max(modelDataDiameterBigRadius)/2
        # self.minRadius = 0.356
        self.minRadius = 0.5

    def getMotorSpeedFromRadius(self, radius, forward, left):
        radius = abs(radius)
        if radius>self.maxRadius:
            return self.getMotorSpeedFromRadiusInfinitRadius(forward)
        elif radius > self.radiusSplitValue:
            return self.getMotorSpeedFromBigRadius(radius, forward, left)
        else:
            if radius < self.minRadius:
                radius = self.minRadius
            return self.getMotorSpeedFromSmallRadius(radius, forward, left)


    def getMotorSpeedFromRadiusInfinitRadius(self, forward):

        multiply = -1
        if forward:
            multiply = 1

        speed = self.motorSpeedToCarSpeed(driveForwardConstantSpeed)*multiply
        gear =0
        motor = [driveForwardConstantSpeed*multiply,driveForwardConstantSpeed*multiply]
        return motor, gear, speed


    def getMotorSpeedFromSmallRadius(self,radius, forward, left):
        outerWheelSpeed = self.getOuterWheelSpeedFromRadius(radius).item()
        innerWheelSpeed = modelDataSpeedInnerWheel

        speed = self.getCarSpeedFromRadius(radius).item()
        return self.getMotorGearAndSpeedFromWheelSpeed(outerWheelSpeed, innerWheelSpeed, speed, forward, left, radius)

    def getMotorSpeedFromBigRadius(self,radius, forward, left):
        outerWheelSpeed = modelDataSpeedOutherWheel
        innerWheelSpeed = self.modelRadiusToCmdSpeedBigRadius(radius).item()

        speed = self.getCarSpeedFromBigRadius(radius).item()
        return self.getMotorGearAndSpeedFromWheelSpeed(outerWheelSpeed, innerWheelSpeed, speed, forward, left, radius)


    def  getMotorGearAndSpeedFromWheelSpeed(self, outerWheelSpeed, innerWheelSpeed, speed, forward, left, radius):
        gear = speed/radius

        if not forward:
            outerWheelSpeed *=-1
            innerWheelSpeed *=-1
            speed *=-1
            gear*=-1

        if left:
            motor = [innerWheelSpeed,outerWheelSpeed]
            gear = -gear
        else:
            motor = [outerWheelSpeed,innerWheelSpeed]

        return motor, gear, speed


    def getOuterWheelSpeedFromRadius(self,radius):
        wheelspeed = self.modelRadiusToCmdSpeed(radius)
        return wheelspeed

    def getInnerWheelSpeedFromBigRadius(self,radius):
        wheelspeed = self.modelRadiusToCmdSpeedBigRadius(radius)
        return wheelspeed

    def getCarSpeedFromRadius(self,radius):
        carSpeed = self.modelRadiusToCarSpeed(radius)
        return carSpeed  

    def getCarSpeedFromBigRadius(self,radius):
        carSpeed = self.modelRadiusToCarSpeedBigRadius(radius)
        return carSpeed  


    def motorSpeedToCarSpeed(self, carSpeed):
        if carSpeed <15:
            return 0
        return 0.0098*carSpeed-0.0668

    def carSpeedToMotorSpeed(self, physSpeed):
        if physSpeed ==0:
            return 0
        return 102.04082*physSpeed+6.81633

    def getMinRadius(self):
        return np.min(modelDataDiameter)/2


if __name__ == "__main__":
    carModel = CarModel()
    motor, gear, speed = carModel.getMotorSpeedFromRadius(0.50, True, True)
    assert motor[0]>0
    assert motor[1]>0
    assert gear<0
    assert motor[0]<motor[1]

    motor, gear, speed = carModel.getMotorSpeedFromRadius(0.50, False, False)
    assert motor[0]<0
    assert motor[1]<0
    assert gear>0
    assert abs(motor[0])>abs(motor[1])

    speed = carModel.getOuterWheelSpeedFromRadius(1.32/2)
    assert speed==50

    speed = carModel.getOuterWheelSpeedFromRadius(0.73/2)
    assert speed==100

    speed = carModel.getOuterWheelSpeedFromRadius(1.21/2)
    np.testing.assert_almost_equal(speed,55)

    motor, gear, speed = carModel.getMotorSpeedFromRadiusInfinitRadius(True)
    assert gear ==0
    assert motor[0] == motor[1]

    speed = carModel.motorSpeedToCarSpeed(carModel.carSpeedToMotorSpeed(40))
    np.testing.assert_almost_equal(speed,40, decimal=3)

    speed = carModel.getOuterWheelSpeedFromRadius(0.6600000000000003)

    radius = np.linspace(0,50,200)
    for r in radius:
        motor, gear, speed = carModel.getMotorSpeedFromRadius(r, True, True)
        print('r:', r, 'li:',motor[0], 're:',motor[1])