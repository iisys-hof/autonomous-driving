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

# This class is inspired by https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/TFLite_detection_webcam.py
class ObjectDetection:

    def __init__(self, objectDetectionNetwork, labelPath):
        self.objectDetectionNetwork = objectDetectionNetwork
        self.labels = self.getLabels(labelPath)

    def analyseImage(self, image):
        boxes, classes, scores = self.objectDetectionNetwork.analyseImage(image)
        imH=image.shape[0]
        imW=image.shape[1]
        pylons = self.filterAndLabelBoxes(boxes, classes, scores, imH, imW )
        return pylons

    def filterAndLabelBoxes(self, boxes, classes, scores, imH, imW, minConfThreshold = 0.5):
        # Loop over all detections and draw detection box if confidence is above minimum threshold
        objects = []
        for i in range(len(scores)):
            if ((scores[i] > minConfThreshold) and (scores[i] <= 1.0)):
                label = str(int(classes[i]))
                if int(classes[i]) < len(self.labels):
                    label = self.labels[int(classes[i])]
                objects.append({
                'ymin': int(max(1,(boxes[i][0] * imH))),
                'xmin': int(max(1,(boxes[i][1] * imW))),
                'ymax': int(min(imH,(boxes[i][2] * imH))),
                'xmax': int(min(imW,(boxes[i][3] * imW))),
                'label': label,
                'score': scores[i]
                })
        return objects


    def getLabels(self, labelPath):
        with open(labelPath, 'r') as f:
            labels = [line.strip() for line in f.readlines()]

            # Have to do a weird fix for label map if using the COCO "starter model" from
            # https://www.tensorflow.org/lite/models/object_detection/overview
            # First label is '???', which has to be removed.
            if labels[0] == '???':
                del(labels[0])
        return labels

