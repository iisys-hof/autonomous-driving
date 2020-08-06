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

from sys import platform


import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
from Controller.NetworkAnalysis.INeuronalNetworkInterpreter import INeuronalNetworkInterpreter
from CrossCutting.TimeMeasurement.TimeMeasurement import TimeMeasurement

class CoralInterpreter(INeuronalNetworkInterpreter):

    def __init__(self, modelPath, imageScaler):
        self.modelPath = modelPath
        self.timeMeasurement = TimeMeasurement("CoralInterpreter")
        self.interpreter =  self.getCoralEdgeTensorflowInterpreter(modelPath)
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.imageScaler = imageScaler

        self.input_shape = self.input_details[0]['shape']
        self.floating_model = (self.input_details[0]['dtype'] == np.float32)



    def getCoralEdgeTensorflowInterpreter(self, modelPath):
        experimental_delegates = [tflite.load_delegate(self.getTensorflowDelegateLibrary())]
        interpreter = tflite.Interpreter(model_path=modelPath + 'detect_edgetpu.tflite', experimental_delegates=experimental_delegates)
        interpreter.allocate_tensors()
        return interpreter

    def getTensorflowDelegateLibrary(self):
        delegateLibrary = 'libedgetpu.so.1'
        if platform == "win32":
            delegateLibrary = 'edgetpu.dll'
        return delegateLibrary


    def getInputShape(self):
        return self.input_shape

    def analyseImage(self, img):
        self.timeMeasurement('resizeImage')
        image = self.imageScaler.scale(img,(self.input_shape[1],self.input_shape[2]))

        self.timeMeasurement('inferenceNetwork')
        self.interpreter.set_tensor(self.input_details[0]['index'], [image])
        self.interpreter.invoke()
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0] # Bounding box coordinates of detected objects
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] # Class index of detected objects
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0] # Confidence of detected objects
        self.timeMeasurement('waite')
        print(self.timeMeasurement, end='')
        return boxes, classes, scores

    def __str__(self):
        text = '################################\n'
        text += 'Coral Interpreter' + '\n'
        text += '################################\n'
        text += 'modelPath: ' + self.modelPath + '\n'
        text += 'inputShape: ' + str(self.getInputShape()) + '\n'
        text += '\n################################\n'
        return text