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

# inspiered by C:\Program Files (x86)\IntelSWTools\openvino_2020.2.117\deployment_tools\inference_engine\samples\python\object_detection_sample_ssd
# cd C:\Program Files (x86)\IntelSWTools\openvino\bin\

from CrossCutting.TimeMeasurement.TimeMeasurement import TimeMeasurement
from openvino.inference_engine import IENetwork, IECore
from Controller.NetworkAnalysis.INeuronalNetworkInterpreter import INeuronalNetworkInterpreter

class NCS2Interpreter(INeuronalNetworkInterpreter):

    def __init__ (self, modelPath, imageScaler):
        self.modelPath = modelPath
        self.timeMeasurement = TimeMeasurement("NCS2Interpreter")
        self.network =  self.getNetwork(modelPath)
        self.interpreterEngine = IECore()
        self.imageScaler = imageScaler

        self.inputBlob = next(iter(self.network.inputs))
        self.outputBlob = next(iter(self.network.outputs))
        self.inputShape = self.network.inputs[self.inputBlob].shape
        self.network.inputs[self.inputBlob].precision = 'U8'
        self.network.outputs[self.outputBlob].precision = "FP32"

        self.interpreter = self.interpreterEngine.load_network(network=self.network, device_name='MYRIAD')

    def getNetwork(self, modelFolder):
        modelPath = modelFolder + 'ssd_mobilenet_v2_coco_fp16.xml'
        weightPath = modelFolder + 'ssd_mobilenet_v2_coco_fp16.bin'
        network = IENetwork(model=modelPath, weights=weightPath)
        return network

    def getInputShape (self):
        return self.inputShape

    def analyseImage(self, img):
        self.timeMeasurement('resizeImage')
        image = self.imageScaler.scale(img, (self.inputShape[3],self.inputShape[2]))


        self.timeMeasurement('inferenceNetwork')
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        networkOutput = self.interpreter.infer(inputs={self.inputBlob: [image]})
        networkOutput = networkOutput[self.outputBlob][0][0]
        self.timeMeasurement('transform output')
        boxes = [detection[3:7] for detection in networkOutput if detection[2]>0]
        classes = [detection[1] for detection in networkOutput if detection[2]>0]
        scores = [detection[2] for detection in networkOutput if detection[2]>0]
        print('adsf')
        print(scores)
        print(classes)
        self.timeMeasurement('getImage')
        print(self.timeMeasurement, end='')
        return boxes, classes, scores
    
    def getVersion(self):
        version =self.interpreterEngine.get_versions('MYRIAD')['MYRIAD']
        version = str(version.major) + '.' + str(version.minor)
        return version

    def getBuildNumber(self):
        version =self.interpreterEngine.get_versions('MYRIAD')['MYRIAD']
        return str(version.build_number)

    def __str__(self):
        text = '################################\n'
        text += 'NCS2 Interpreter' + '\n'
        text += '################################\n'
        text += 'modelPath: ' + self.modelPath + '\n'
        text += 'inputShape: ' + str(self.getInputShape()) + '\n'
        text += 'version: ' + self.getVersion() + '\n'
        text += 'build version: ' + self.getBuildNumber() + '\n'
        text += '\n################################\n'
        return text
