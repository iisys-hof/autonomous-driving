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

import json
import time
from sys import platform
import serial


class MoveControllerCommunication:
    def __init__(self,carModel, com = None, baudrate= 9600, changeMoveCallback = None):
        self.radiusBig = 0.55
        self.radiusSmall = 0.365
        self.error = False
        self.carModel = carModel
        self.changeMoveCallback = changeMoveCallback
        if com is None:
            if platform == "win32":
                com = 'COM7'
            else:
                com ='/dev/ttyACM0'
        try:
            self.communication = serial.Serial(com, baudrate= 9600, 
            timeout=2.5, 
            parity=serial.PARITY_NONE, 
            bytesize=serial.EIGHTBITS, 
            stopbits=serial.STOPBITS_ONE)

            time.sleep(1)
            self.communication.reset_input_buffer()
        except:
            print('Error: No Move controller available over port ' + com)
            self.error = True

    def turnLeft(self):
        self.driveCircle(self.radiusSmall,True, True)

    def turnRight(self):
        self.driveCircle(self.radiusSmall,True, False)

    def drive(self):
        self.driveCircle(float('inf'),True, False)

    def driveLeft(self):
        self.driveCircle(self.radiusBig,True, True)

    def driveRight(self):
        self.driveCircle(self.radiusBig,True, False)

    def backwardLeft(self):
        self.driveCircle(self.radiusBig,False, True)

    def backwardRight(self):
        self.driveCircle(self.radiusBig,False, False)

    def backward(self):
        self.driveCircle(float('inf'), False, False)

    def stop(self):
        if self.changeMoveCallback is not None:
            self.changeMoveCallback(0, 0)
        self.move([0,0])

    def fullLeft(self):
        self.move([-100,100])
        time.sleep(0.2)
        self.stop()

    def driveCircle(self,  radius, forward, left):
        motor, gear, speed = self.carModel.getMotorSpeedFromRadius(radius, forward, left)
        print('l:', round(motor[0]), 'r:', round(motor[1]), 'g:', round(gear,4), 's:', round(speed,4))
        if self.changeMoveCallback is not None:
            self.changeMoveCallback(gear, speed)
        self.move(motor)

    def move(self, motor):
        if not self.error:
            command = {}
            command["command"] = "move"
            command["left"] = int(motor[0])
            command["right"] = int(motor[1])
            self.communication.write(json.dumps(command).encode('ascii'))


    def getSonic(self):
        if not self.error:
            inputBuffer = self.communication.readline()


            command = {}
            command["command"] = "sonic"
            self.communication.write(json.dumps(command).encode('ascii'))
            try:
                sonic = json.loads(inputBuffer)
                return sonic
            except:
                print("exception in get Sonic")
                return {"left": 0, "right": 0, "middle":0}
