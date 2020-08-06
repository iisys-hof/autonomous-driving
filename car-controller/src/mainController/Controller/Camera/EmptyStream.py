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
import math
import numpy as np

class EmptyStream(ICamera):
    _h = 480
    _w = 640
    angleWidth = 60
    def __init__(self,path=None):pass
    def run(self):
        while True:
            image = np.zeros((self._h,self._w,3),dtype=np.uint8)
            deepMap = np.zeros((self._h,self._w),dtype=np.uint16)
            yield image,deepMap, None
    def stop(self):pass
    def getAngleWidth(self):
        angleWidth = self.angleWidth* math.pi /180
        return angleWidth

    def __str__(self):
        text = '################################\n'
        text += 'Empty Stream Camera' + '\n'
        text += '################################\n'
        text += 'Width: ' + str(self._h) + '\n'
        text += 'Height: ' + str(self._w) + '\n'
        text += 'angleWidth: ' + str(self.angleWidth) + '\n'
        text += 'Deep Image: True' + '\n'
        text += '\n################################\n'
        return text
