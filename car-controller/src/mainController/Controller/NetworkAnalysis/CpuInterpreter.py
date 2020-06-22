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

import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
from Controller.NetworkAnalysis.INeuronalNetworkInterpreter import INeuronalNetworkInterpreter
from CrossCutting.TimeMeasurement.TimeMeasurement import TimeMeasurement

class CpuInterpreter(INeuronalNetworkInterpreter):
    def __init__(self,modelPath, imageScaler):
        self.modelPath = modelPath
        self.timeMeasurement = TimeMeasurement("CpuInterpreter")
        self.interpreter =  self.getInterpreter(modelPath)
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.imageScaler = imageScaler

        self.input_shape = self.input_details[0]['shape']
        self.floating_model = (self.input_details[0]['dtype'] == np.float32)


    def getInterpreter(self, modelPath):
        interpreter =  tflite.Interpreter(model_path = modelPath + 'detect.tflite')
        interpreter.allocate_tensors()
        return interpreter
    
    def getInputShape(self):
        return self.input_shape

    def analyseImage(self, img):
        self.timeMeasurement('resizeImage')
        image = self.imageScaler.scale(img,(self.input_shape[1],self.input_shape[2]))

        self.timeMeasurement('inferenceNetwork')
        if self.floating_model:
            image = (np.float32(image) - 128.0) / 128.0
        self.interpreter.set_tensor(self.input_details[0]['index'], [image])
        self.interpreter.invoke()
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0] # Bounding box coordinates of detected objects
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] # Class index of detected objects
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0] # Confidence of detected objects


        self.timeMeasurement('getImage')
        print(self.timeMeasurement, end='')
        return boxes, classes, scores

    def __str__(self):
        text = '################################\n'
        text += 'CPU Interpreter' + '\n'
        text += '################################\n'
        text += 'modelPath: ' + self.modelPath + '\n'
        text += 'inputShape: ' + str(self.getInputShape()) + '\n'
        text += 'floatingModel: ' + str(self.floating_model) + '\n'
        text += '\n################################\n'
        return text