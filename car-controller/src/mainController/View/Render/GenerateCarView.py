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


import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

import cv2


# This class is inspired by https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/TFLite_detection_webcam.py
class GenerateCarView:

    def __init__(self):
        self.frameRateCalc = 1
        self.freq = cv2.getTickFrequency()
        self.t1 = cv2.getTickCount()
        

    def getFrame(self, image, pylons= None):
        # self.addFrameRate(image)

        if pylons is not None:
            self.addBoxesToImage(image, pylons)
        return image

    def addFrameRate(self,image):
        cv2.putText(image,'FPS: {0:.2f}'.format(self.frameRateCalc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
        self.t2 = cv2.getTickCount()
        self.frameRateCalc = self.freq/(self.t2-self.t1)
        self.t1 = cv2.getTickCount()


    def addBoxesToImage(self, image, pylons):
        for pylone in pylons:
            xmin = pylone['xmin']
            ymin = pylone['ymin']
            xmax = pylone['xmax']
            ymax = pylone['ymax']
            cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

            # Draw label
            label = pylone['label'] + ' %d%%' % (int(pylone['score']*100)) + ' ' + str(round(pylone['distanceAbsolut'],2)) + ' m'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
