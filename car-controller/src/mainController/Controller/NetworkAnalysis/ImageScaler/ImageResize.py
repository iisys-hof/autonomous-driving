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

from Controller.NetworkAnalysis.ImageScaler.IImageScaler import IImageScaler

import cv2

class ImageResize(IImageScaler):
    def scale (self, image, outputShape):
        imageScaled = cv2.resize(image,outputShape)
        imageChangedColor   = cv2.cvtColor(imageScaled,cv2.COLOR_RGB2BGR)
        return imageChangedColor

    def __str__(self):
        text = '################################\n'
        text += 'ImageResize' + '\n'
        text += '################################\n'
        text += 'resize FrameWork: cv2' + '\n'
        text += 'compression: INTER_LINEAR' + '\n'
        text += '\n################################\n'
        return text