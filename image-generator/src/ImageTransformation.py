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
import numpy as np

class ImageTransformation:

    def getMaskFromGreenscreen(self, picture):
        image = cv2.cvtColor(picture, cv2.COLOR_BGR2HSV)
        dark_green = np.array([30, 80, 80], dtype='uint8')
        bright_green = np.array([100, 255, 255], dtype='uint8')
        black_mask = cv2.inRange(image, dark_green, bright_green)
        mask = cv2.bitwise_not(black_mask)
        mask = cv2.merge((mask, mask, mask))
        return mask


    def getRandomRotatedImage(self, image):
        angle = np.random.randint(-10, 10)
        shape = image.shape
        M = cv2.getRotationMatrix2D((shape[0]/2, shape[1]/2), angle, 1)
        return cv2.warpAffine(image, M, (shape[1], shape[0]), borderValue=(66, 166, 66))


    def resizeImage(self, image, distance):
        return cv2.resize(image, (0, 0), fx=distance, fy=distance)

    def scale(self, image):
        scaleFactor = np.random.uniform(0.7,1.5)
        oldDimension = image.shape
        newDimension = (oldDimension[1], int(oldDimension[0]* scaleFactor))
        resized = cv2.resize(image, newDimension, interpolation = cv2.INTER_AREA)
        return resized