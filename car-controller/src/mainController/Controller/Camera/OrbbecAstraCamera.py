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

import os

from Controller.Camera.ICamera import ICamera

import numpy as np
from primesense import _openni2 as c_api
from primesense import openni2

import math
import cv2

class OrbbecAstraCamera(ICamera):
    _rgb_stream = None 
    _depth_stream = None
    _dev = None
    _h = 480
    _w = 640
    frameRate = 30
    angleWidth = 60
    openNIDist= None


    def __init__(self,openNIDist=None):
        self.error = False
        if not openni2.is_initialized():
            dist = openNIDist
            if dist is None:
                if 'OPENNI2_REDIST64' in os.environ:
                    dist = os.environ['OPENNI2_REDIST64']
                if 'OPENNI2_REDIST' in os.environ:
                    dist = os.environ['OPENNI2_REDIST']
            if dist is not None:
                self.openNIDist = dist
                openni2.initialize(dist) 
        if not openni2.is_initialized():
            raise Exception("openNI2 not initialized form path: " + str(openNIDist))
        
        self._dev = openni2.Device.open_any()
    
    def run(self):
        self._rgb_stream = self._dev.create_color_stream()
        self._depth_stream = self._dev.create_depth_stream()

        self._rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=self._w, resolutionY=self._h, fps=self.frameRate))
        self._depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=self._w, resolutionY=self._h, fps=self.frameRate))

        self._depth_stream.set_mirroring_enabled(False)
        self._rgb_stream.set_mirroring_enabled(False)

        self._rgb_stream.start()
        self._depth_stream.start()

        # Synchronize the streams
        self._dev.set_depth_color_sync_enabled(True) # synchronize the streams

        # IMPORTANT: ALIGN DEPTH2RGB (depth wrapped to match rgb stream)
        self._dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)


        return self.getStream()

    def getAngleWidth(self):
        angleWidth = self.angleWidth* math.pi /180
        return angleWidth
        
    def stop(self):
        self._rgb_stream.stop()
        print('Closed color stream')

        self._depth_stream.stop()
        print('Closed depth stream')

        openni2.unload()
        print('Unloaded OpenNI2')

    def getStream(self):
        while True:
            yield self.takePicture()

    def takePicture(self):
        image   = np.fromstring(self._rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(self._h,self._w,3)
        image   = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        deepMap = np.fromstring(self._depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(self._h,self._w)
        return image,deepMap, None


    def __str__(self):
        text = '################################\n'
        text += 'OrbbecAstra Camera' + '\n'
        text += '################################\n'
        text += 'Width: ' + str(self._h) + '\n'
        text += 'Height: ' + str(self._w) + '\n'
        text += 'FPS: ' + str(self.frameRate) + '\n'
        text += 'angleWidth: ' + str(self.angleWidth) + '\n'
        text += 'Deep Image: True' + '\n'

        text += 'openNIDist: ' + self.openNIDist + '\n'
        text += '\n################################\n'
        return text
