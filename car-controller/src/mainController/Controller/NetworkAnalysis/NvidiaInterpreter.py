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

import jetson.inference

from Controller.NetworkAnalysis.INeuronalNetworkInterpreter import INeuronalNetworkInterpreter
from CrossCutting.TimeMeasurement.TimeMeasurement import TimeMeasurement

class NvidiaInterpreter(INeuronalNetworkInterpreter):
    def __init__(self,modelPath, imageScaler):
        self.model = 'ssd-mobilenet-v2'
        self.timeMeasurement = TimeMeasurement("NvidiaInterpreter")
        self.session =  jetson.inference.detectNet(self.model,threshold =0.05)
        self.input_shape = [1,300,300,3]

    def getInputShape(self):
        return self.input_shape

    def analyseImage(self, inputImage):
        self.timeMeasurement('inferenceNetwork and resize')
        image, width, height = inputImage
        output = self.session.Detect(image,width,height)

        self.timeMeasurement('transformResults')
        print(self.timeMeasurement, end='')
        # outputSorted = self.sortOutputs(output)
        boxes, classes, scores = self.extractResults(output, width, height)

        self.timeMeasurement('getImage')
        return boxes, classes, scores

    def sortOutputs(self, output):
        output.sort(key=lambda x: x.Confidence, reverse=True)
        output = output[:10]
        return output

    def extractResults(self, networkOutput, width, height):
        boxes =[]
        classes=[]
        scores=[]
        for detection in networkOutput:
            classes.append(detection.ClassID)
            scores.append(detection.Confidence)
            boxes.append([detection.Top/height, detection.Left/width, detection.Bottom/height,  detection.Right/width])
        return boxes, classes, scores


    def __str__(self):
        text = '################################\n'
        text += 'NvidiaInterpreter Interpreter' + '\n'
        text += '################################\n'
        text += 'model: ' + self.model + '\n'
        text += 'inputShape: ' + str(self.getInputShape()) + '\n'
        text += '\n################################\n'
        return text