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

import numpy as np
import cv2

class ImageNoise:
    def addNoise(self,image):
        kindOfNoise = ['gauss','s&p','poisson','speckle']
        choice = np.random.randint(0,len(kindOfNoise))
        noisyImage  = self.noisy(kindOfNoise[choice],image)
        noisyImage = noisyImage.astype(np.uint8)
        return noisyImage

    def noisy(self, noise_typ,image):
        if noise_typ == 'gauss':
            return self.noisyGauss(image)
        elif noise_typ == 's&p':
            return self.noisySaltAndPepper(image)
        elif noise_typ == 'poisson':
            return self.noisyPoisson(image)
        elif noise_typ =='speckle': 
            return self.noisySpeckle(image)
        return image

    def noisySpeckle(self, image):
        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss *np.random.uniform(0.001,0.01)
        return noisy

    def noisyPoisson(self, image):
        countUniqueElements = len(np.unique(image))
        countUniqueElements = 2 ** np.ceil(np.log2(countUniqueElements))
        noisy = np.random.poisson(image * countUniqueElements) / float(countUniqueElements)
        return noisy

    def noisySaltAndPepper(self, image):
        amount = np.random.uniform(0.001,0.01)
        out = np.copy(image)
        countOfPixelErrors = np.ceil(amount * image.size)
        coords = [np.random.randint(0, i - 1, int(countOfPixelErrors)) for i in image.shape[:2]]
        out[coords] = 255
        coords = [np.random.randint(0, i - 1, int(countOfPixelErrors)) for i in image.shape[:2]]
        out[coords] = 0
        return out


    def noisyGauss(self, image):
        row,col,ch= image.shape
        mean = 0
        var = 0.00001
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch )*255
        gauss = gauss.astype(image.dtype)
        noisy = cv2.add(image,gauss)
        return noisy