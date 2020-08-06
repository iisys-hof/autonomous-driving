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

class ImageChangeColor:

    def changeGamma(self, image):
        gamma = np.random.uniform(0.5,1.5)
        invGamma = 1.0 / gamma
        lookupTableGammaChange = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

        gammaChangedImage = cv2.LUT(image, lookupTableGammaChange)
        return gammaChangedImage

    def changeColor(self,image):
        transformedImage = self.ImageToHLS(image)
        changeFactor = np.random.randint(-3, 10)
        transformedImage[:,:,]  += changeFactor
        image = self.ImageFromHLS(transformedImage)
        return image
       
    def changeBrightness(self, image):
        transformedImage = self.ImageToHLS(image)
        changeFactor = np.random.randint(-100, 100)
        transformedImage[:,:,1]  += changeFactor
        returnImage = self.ImageFromHLS(transformedImage)
        return returnImage
       


    def ImageToHLS(self, image):
        transformedImage = cv2.cvtColor(image, cv2.COLOR_RGB2HLS).astype(np.int)
        return transformedImage

    def ImageFromHLS(self, image):
        image[image<0] =0
        image[image>255] =255
        image =image.astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_HLS2RGB)
        return image