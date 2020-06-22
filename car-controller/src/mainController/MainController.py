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


import logging
import queue
import sys
import time
from sys import platform

import numpy as np
import requests
import math
import pickle

from CrossCutting.TimeMeasurement.TimeMeasurement import TimeMeasurement

from Controller.AreaMap.AreaMap import AreaMap
from Controller.MoveController.MoveController import MoveController
from Controller.ObjectDetection.ObjectDetection import ObjectDetection
from Controller.ObjectDetection.ObjectDistance import ObjectDistance
from Controller.TrajectoryPlanning.TrajectoryPlanning import TrajectoryPlanning
from Controller.NetworkAnalysis.ImageScaler.ImageResize import ImageResize

from Generator.CameraGenerator import CameraGenerator
from Generator.NeuronalNetworkInterpreterGenerator import NeuronalNetworkInterpreterGenerator

from Workflows.HomepageServerThread import HomepageServerThread
from Workflows.ImageRenderThread import ImageRenderThread

modelName = 'ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03'

if platform == "win32":
    basePath = 'D:/Projekte/'
else:
    basePath ='/home/pi/'

localPath = 'autonomous-driving/trained-networks/'
modelPath = basePath + localPath + modelName + '/'
labelPath = basePath + localPath + modelName + '/labelmap.txt'

class MainController:
    def __init__(self, angleWidthCamera):
        self.timeMeasurement = TimeMeasurement("Main Controller")
        self.toRenderQueue = queue.Queue(maxsize = 1)
        self.manualMovementQueue = queue.Queue(maxsize = 5)
        self.automaticMovementQueue = queue.Queue(maxsize = 1)
        self.moveControllerCommandQueue = queue.Queue(maxsize = 5)
        self.trajectoryPlanningCommandQueue = queue.Queue(maxsize = 5)
        

        self.imageRenderThread = ImageRenderThread(self.toRenderQueue)
        renderedImageQueue = self.imageRenderThread.getRenderedQueue()

        self.homepageServerThread = HomepageServerThread(renderedImageQueue, self.manualMovementQueue, self.moveControllerCommandQueue, self.trajectoryPlanningCommandQueue)
        
        self.moveControllerThread = MoveController(self.automaticMovementQueue,self.manualMovementQueue, self.moveControllerCommandQueue)
        realMovementQueue = self.moveControllerThread.getRealMovementQueue()
        emergencyStopQueue = self.moveControllerThread.getEmergencyStopQueue()
        

        self.areaMap = AreaMap(realMovementQueue, angleWidthCamera)
        self.trajectoryPlanning = TrajectoryPlanning(self.areaMap, emergencyStopQueue )
        imageScaler = ImageResize()
        networkInterpreter = NeuronalNetworkInterpreterGenerator().getInterpreter(modelPath, imageScaler)
        print(networkInterpreter)
        self.objectDetection = ObjectDetection(networkInterpreter,labelPath)
        self.objectDistance = ObjectDistance(angleWidthCamera)
        print('#############init ready##########################')

    def run(self, stream):
        self.imageRenderThread.start()
        self.moveControllerThread.start()
        self.homepageServerThread.start()
        try:
            for imgColor, imgDeep, imageId  in stream:
                self.timeMeasurement('handle trajectoryPlanningCommandQueue')

                if not self.trajectoryPlanningCommandQueue.empty():
                    command = self.trajectoryPlanningCommandQueue.get()
                    if command == 'reset_map':
                        self.areaMap.reset()
                        self.trajectoryPlanning.reset()
                
                imgColor, pylons = self.handleImage(imgColor, imgDeep )
                self.timeMeasurement('send image')
                self.sendImage(imgColor, pylons)

                self.timeMeasurement('getImagefromStream')
                print(self.timeMeasurement, end='')
        except:
            self.shutdownThreads()
            logging.exception("message")


    def handleImage(self, imgColor, imgDeep):
        self.timeMeasurement('object detection')
        pylons = self.objectDetection.analyseImage(imgColor)
        self.timeMeasurement('object distance')
        self.objectDistance.addDistance(pylons,imgColor, imgDeep)

        self.timeMeasurement('updatePylons')
        self.areaMap.updatePylons(pylons)

        self.timeMeasurement('trajectoryPlanning.nextMove')
        nextMove = self.trajectoryPlanning.nextMove()

        self.timeMeasurement('handle automaticMovementQueue')
        if not self.automaticMovementQueue.full():
            self.automaticMovementQueue.put_nowait(nextMove)
        
        return imgColor, pylons

    def sendImage(self, imgColor, pylons):
        if not self.toRenderQueue.full():
            self.toRenderQueue.put_nowait([imgColor,pylons, self.areaMap, self.trajectoryPlanning, angleWidthCamera])

    def shutdownThreads(self):
        print('shut down threads')
        self.moveControllerCommandQueue.put_nowait('kill')
        requests.get('http://127.0.0.1:5000/shutdown')

if __name__ == '__main__':
    camera = CameraGenerator().getCamera()
    print(camera)
    angleWidthCamera = camera.getAngleWidth()
    imageStream = camera.run()

    mainController = MainController(angleWidthCamera)
    mainController.run(imageStream)
