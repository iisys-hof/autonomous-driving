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

import cv2
from os import listdir

class ImageLoader:
    def loadOneImage(self, path):
        image = cv2.imread(path)
        return image

    def getFileList(self, path):
        return listdir(path)

    def loadImagesFromPath(self, imagePath):
        paths = self.getFileList(imagePath)
        return [self.loadOneImage(imagePath + path) for path in paths]

        