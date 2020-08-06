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

import time
import math
from os import listdir

from Controller.Camera.ICamera import ICamera

import jetson.utils


class JetsonLocalFileStream(ICamera):
    angleWidth = 60
    def __init__(self, path):
        self.path = path
        self.paths = self.getFileList(self.path)
        self.images = self.loadImages()

    def run(self):
        for image in self.images:
            yield image['image'], None, image['file']

    def getAngleWidth(self):
        angleWidth = self.angleWidth* math.pi /180
        return angleWidth

    def loadImageFromPath(self, path):
        image = jetson.utils.loadImageRGBA(path)
        return image

    def getFileList(self, path):
        return listdir(path)

    def loadImages(self):
        for path in self.paths:
            if path.endswith('.png') or path.endswith('.jpg'):
                yield {
                    'image': self.loadImageFromPath(self.path + path),
                    'file': path
                }
                    


    def __str__(self):
        text = '################################\n'
        text += 'Jetson Local File Stream' + '\n'
        text += '################################\n'
        text += 'angleWidth: ' + str(self.angleWidth) + '\n'
        text += 'Deep Image: False' + '\n'
        text += 'Count Images:' + str(len(self.paths)) + '\n'
        text += '\n################################\n'
        return text