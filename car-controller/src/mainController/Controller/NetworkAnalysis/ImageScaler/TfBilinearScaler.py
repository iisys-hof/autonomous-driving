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

from Controller.NetworkAnalysis.ImageScaler.IImageScaler import IImageScaler

import tensorflow as tf
import cv2
import numpy as np
from multiprocessing import Pool


config = tf.ConfigProto(
        device_count = {'GPU': 0}
    )

class TfBilinearScaler(IImageScaler):
    def scale (self, image, outputShape):
        with Pool(1) as p:
            return p.apply(scaleWorker, (image,outputShape))

    def __str__(self):
        text = '################################\n'
        text += 'TfBilinearScaler' + '\n'
        text += '################################\n'
        text += 'resize FrameWork: tensorflow' + '\n'
        text += 'compression: BILINEAR' + '\n'
        text += '\n################################\n'
        return text

def scaleWorker (image, outputShape):
    imageScaled = tf.image.resize_images(image, tf.stack(outputShape),method=tf.image.ResizeMethod.BILINEAR,align_corners=False)
    tfSession = tf.Session(config=config)
    imageDecoded = tfSession.run(imageScaled)
    imageDecoded = imageDecoded.astype(np.uint8)
    imageChangedColor   = cv2.cvtColor(imageDecoded,cv2.COLOR_RGB2BGR)
    return imageChangedColor
