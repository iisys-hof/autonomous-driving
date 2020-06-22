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
from Controller.Camera.ICamera import ICamera
import math

# for the frames you have to use a combination found here: https://www.logitech.com/de-de/product/brio#specification-tabular
possibleCameraConfigurations = {
    '4k': {'framesPerSecond': 30, 'frameHigh': 4096, 'frameWidth': 2160},
    'fullHD': {'framesPerSecond': 60, 'frameHigh': 1920, 'frameWidth': 1080 },
    'HD': {'framesPerSecond': 90, 'frameHigh': 1280, 'frameWidth': 720},
    'SD': {'framesPerSecond': 90, 'frameHigh': 640, 'frameWidth': 480}
}

class LogitechCamera(ICamera):
    angleWidth = 82.1
    chosenCameraConfiguration = 'SD'
    def __init__(self,path=None):
        cameraConfiguration = possibleCameraConfigurations[self.chosenCameraConfiguration]
        self.videoCapture = self.initVideoDriver(**cameraConfiguration)
        if not self.videoCapture.isOpened():
            raise Exception("could not open a logitech camera")


    def run(self):
        while True:
            yield self.takePicture(), None, None

    def takePicture(self):
        success, image = self.videoCapture.read()
        if success is False:
            raise Exception("logitech camera stream get broken during usage. Be sure the USB is stil connected")

        image   = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        return image

    '''
    Here i have a lot of problems with the init of the videoCapture
    we use 2 Times set FPS because in some situations it works at start and in some it works at the end. But i does not demage if we use it more times.
    To solve it you could try this:
    1) use print(self.getPossibleVideoDriverIDs()) to find out wich id you have to use in cv2.VideoCapture(id)
    2) If the camera connects and the fps could not been changed, you can try to switch the order of the set commands
    '''
    def initVideoDriver(self, framesPerSecond, frameHigh, frameWidth):
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        videoCapture = cv2.VideoCapture(200)
        videoCapture.set(cv2.CAP_PROP_FPS, framesPerSecond)
        videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH , frameHigh)
        videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT , frameWidth)
        videoCapture.set(cv2.CAP_PROP_FOURCC, fourcc)
        videoCapture.set(cv2.CAP_PROP_FPS, framesPerSecond)
        return videoCapture

    def stop(self):
        self.videoCapture.release()

    def getAngleWidth(self):
        angleWidth = self.angleWidth* math.pi /180
        return angleWidth

    def __str__(self):
        text = '################################\n'
        text += 'Logitech Camera' + '\n'
        text += '################################\n'
        text += 'Width: ' + str(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)) + '\n'
        text += 'Height: ' + str(self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)) + '\n'
        text += 'FPS: ' + str(self.videoCapture.get(cv2.CAP_PROP_FPS)) + '\n'
        text += 'Decoding: ' + str(self.videoCapture.get(cv2.CAP_PROP_FOURCC)) + '\n'
        text += 'angleWidth: ' + str(self.angleWidth) + '\n'
        text += 'Deep Image: False' + '\n'
        text += '\n################################\n'
        return text

    def getPossibleVideoDriverIDs(self):
        videoDriverIDs = [ids for ids in range(1000) if cv2.VideoCapture(ids).isOpened()]
        return videoDriverIDs