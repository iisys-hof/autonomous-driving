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

import logging
import threading
import time
import queue

from Controller.MoveController.CarModel import CarModel
from Controller.MoveController.DriveCurve import DriveCurve
from Controller.MoveController.MoveControllerCommunication import MoveControllerCommunication


class MoveController(threading.Thread):
    def __init__(self, automaticMovementQueue, manualMovementQueue, commandQueue):
        super(MoveController, self).__init__()
        self.realMovementQueues = queue.Queue(maxsize = 20)
        self.emergencyStopQueue = queue.Queue(maxsize = 1)
        self.carModel = CarModel()
        self.moveControllerCommunication = MoveControllerCommunication(self.carModel, changeMoveCallback=lambda gear, speed: self.realMovementQueues.put_nowait({'gear':gear,'speed': speed, 'time': time.time()}) if not self.realMovementQueues.full() else None)
        self.driveCurve = DriveCurve(self.carModel)
        self.automaticMovementQueue = automaticMovementQueue
        self.manualMovementQueue = manualMovementQueue
        self.commandQueue = commandQueue
        self.mode = False
        self.emergencyMode = False
        self.safetyOutside = 5
        self.safetyMiddle = 15

    def getRealMovementQueue(self):
        return self.realMovementQueues

    def getEmergencyStopQueue(self):
        return self.emergencyStopQueue

    def run(self):
        while True:
            try:
                if self.isEmergencyStop():
                    if not self.emergencyStopQueue.full():
                        self.emergencyStopQueue.put_nowait(True)
                    if not self.emergencyMode:
                        self.emergencyMode = True
                        self.driveCurve.setCurve({'x':0, 'y': 0, 'm':0})
                        self.automaticMovementQueue.queue.clear()
                        self.moveControllerCommunication.stop()

                self.setCommandIfAvailable()
   
                if self.mode == 'autonomous_driving':
                    self.setAutomaticMove()
                        

                if self.mode == 'manuel_driving':
                    self.manualMove()

                if self.mode == 'curve_test_mode':
                    self.updateCurveRadius()
            
            except:
                logging.exception("message")
            time.sleep(0.04)
    
    def setAutomaticMove(self):
        if not self.automaticMovementQueue.empty():
            automaticMove = self.automaticMovementQueue.get()
            if 'command' in automaticMove:
                if automaticMove['command'] == 'resetSavety':
                    self.setDriveMode('autonomous_driving')

                if automaticMove['command'] == 'turnLeft':
                    self.moveControllerCommunication.fullLeft()
                    time.sleep(1)

            else:
                self.driveCurve.setCurve(automaticMove)
                self.updateCurveRadius()


    def setCurveTest(self):
        self.driveCurve.setCurve({'x':1, 'y': 1, 'm':0})

    def updateCurveRadius(self):
        if self.driveCurve.isDriving():
            radius = self.driveCurve.getNextRadius()

            left = True
            if radius>0:
                left = False
            self.moveControllerCommunication.driveCircle(abs(radius), True, left)
        else:
            self.moveControllerCommunication.stop()
        time.sleep(0.1)

    def manualMove(self):
        if not self.manualMovementQueue.empty():
            manualMove = self.manualMovementQueue.get()

            if manualMove['up'] is True:
                if manualMove['left'] is True:
                    self.moveControllerCommunication.driveLeft()
                elif manualMove['right'] is True:
                    self.moveControllerCommunication.driveRight()
                else:
                    self.moveControllerCommunication.drive()

            elif manualMove['down'] is True:
                if manualMove['left'] is True:
                    self.moveControllerCommunication.backwardLeft()
                elif manualMove['right'] is True:
                    self.moveControllerCommunication.backwardRight()
                else:
                    self.moveControllerCommunication.backward()
                    
            elif manualMove['left'] is True:
                self.moveControllerCommunication.turnLeft()

            elif manualMove['right'] is True:        
                self.moveControllerCommunication.turnRight()

            else:
                self.moveControllerCommunication.stop()


    def isEmergencyStop(self):
        emergencyStop = False
        sonic = self.moveControllerCommunication.getSonic()
        if sonic is None:
            return False
        if self.safetyOutside > sonic['left'] >0:
            emergencyStop =  True
        if self.safetyOutside > sonic['right'] >0:
            emergencyStop = True
        if self.safetyMiddle > sonic['middle'] >0:
            emergencyStop =   True
        if emergencyStop:
            print(emergencyStop,sonic)
        return emergencyStop

    def setCommandIfAvailable(self):
        if not self.commandQueue.empty():
            command = self.commandQueue.get()
            if command == 'kill':
                return
            self.setDriveMode(command)
            if command == 'curve_test_mode':
                self.setCurveTest()

    def setDriveMode(self, command):
        self.mode = command
        self.automaticMovementQueue.queue.clear()
        self.manualMovementQueue.queue.clear()
        self.moveControllerCommunication.stop()
        self.emergencyMode = False