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

from Controller.Camera.ICamera import ICamera
import jetson.utils
import math

# for the frames you have to use a combination found here: https://www.logitech.com/de-de/product/brio#specification-tabular
possibleCameraConfigurations = {
    '4k': {'framesPerSecond': 30, 'frameHigh': 4096, 'frameWidth': 2160},
    'fullHD': {'framesPerSecond': 60, 'frameHigh': 1920, 'frameWidth': 1080 },
    'HD': {'framesPerSecond': 90, 'frameHigh': 1280, 'frameWidth': 720},
    'SD': {'framesPerSecond': 90, 'frameHigh': 640, 'frameWidth': 480}
}

class JetsonCamera(ICamera):
    angleWidth = 82.1
    chosenCameraConfiguration = 'SD'
    def __init__(self,path=None):
        self.cameraConfiguration = possibleCameraConfigurations[self.chosenCameraConfiguration]
        # use this to find camera id: v4l2-ctl --list-devices
        self.camera = jetson.utils.gstCamera(self.cameraConfiguration['frameHigh'], self.cameraConfiguration['frameWidth'], '/dev/video0')
        try:
            self.takePicture()
        except:
            raise Exception("could not open a camera with Jetson")


    def run(self):
        while True:
            yield self.takePicture(), None, None

    def takePicture(self):
        image, width, height = self.Controller.Camera.CaptureRGBA()
        return [image, width, height]

    def getAngleWidth(self):
        angleWidth = self.angleWidth* math.pi /180
        return angleWidth

    def __str__(self):
        text = '################################\n'
        text += 'Jetson Camera' + '\n'
        text += '################################\n'
        text += 'Width: ' + str( self.cameraConfiguration['frameWidth']) + '\n'
        text += 'Height: ' + str(self.cameraConfiguration['frameHigh']) + '\n'
        text += 'FPS: ' + str(self.cameraConfiguration['framesPerSecond']) + '\n'
        text += 'angleWidth: ' + str(self.angleWidth) + '\n'
        text += 'Deep Image: False' + '\n'
        text += '\n################################\n'
        return text