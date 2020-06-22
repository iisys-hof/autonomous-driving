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

from .GenerateBirdView import GenerateBirdView
from .GenerateCarView import GenerateCarView
from CrossCutting.TimeMeasurement.TimeMeasurement import TimeMeasurement


class RenderImage:
    def __init__(self):
        self.generateCarView = GenerateCarView()
        self.generateBirdView = GenerateBirdView()
        self.timeMeasurement = TimeMeasurement("ImageRenderThread", 100)


    def getFrame(self, image, pylons, areaMap, trajectoryPlanning, angleWidthCamera):

        self.timeMeasurement('render car view')
        carView = self.generateCarView.getFrame(image,pylons)
        imH=image.shape[0]
        imW=image.shape[1]
        self.timeMeasurement('render bird view')
        birdView = self.generateBirdView.getFrame(imH, imW, areaMap, trajectoryPlanning, angleWidthCamera)
        self.timeMeasurement('merge images')
        image = np.concatenate((carView, birdView), axis=1)
        self.timeMeasurement('wait')
        print(self.timeMeasurement, end='')
        return image
