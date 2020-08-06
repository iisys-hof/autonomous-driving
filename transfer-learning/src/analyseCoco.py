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

from object_detection.metrics import coco_evaluation
from object_detection.utils import label_map_util
import json
import tensorflow as tf
from google.protobuf.json_format import MessageToJson
from object_detection.data_decoders.tf_example_decoder import TfExampleDecoder
import numpy as np
from os import path
from multiprocessing import Pool

basePath = 'D:/Projekte/autonomous-driving/'
cocoPath = basePath + 'working/coco/'
LabelMapPath = basePath + 'transfer-learning/src/object_detection/data/mscoco_complete_label_map.pbtxt'
validationPath =  basePath + 'paper-energy-consumption/coco/NvidiaJetsonFloatcocoValidation.json'
maxIterations = 5000
tfExampleDecoder = TfExampleDecoder()
config = tf.ConfigProto(
        device_count = {'GPU': 0}
    )


def main(unused_argv):
    evaluator = createEvaluator(LabelMapPath)
    grundTruthJson = loadGroundTruthJson(cocoPath + 'TFRecord/')
    addGrundTruthToEvaluator(evaluator, grundTruthJson)
    addDetectedImageInfoToEvaluator(evaluator, validationPath)
    print('evaluate ###########################')
    metrics = evaluator.evaluate()
    # evaluator.dump_detections_to_json_file(json_output_path=cocoPath + 'cocoResult.json')
    print(metrics)

def loadGroundTruthJson(cocoPath):
    cocoJson = cocoPath + 'GroundTruth.json'
    if path.isfile(cocoJson):
        print('using json')
        with open(cocoJson) as jsonFile:
            return json.load(jsonFile)
    print('generating json')
    grundTruthJson = generateGroundTruthJson( cocoPath + 'coco_val.record')
    with open(cocoJson, 'w', encoding='utf-8') as f:
        json.dump(grundTruthJson, f, cls=NumpyEncoder, indent=2)
    return grundTruthJson


def generateGroundTruthJson(tfRecordPath):
    tfRecord = openTFRecord(tfRecordPath)
    grundTruthJson = []
    for index, tfRecordPart in enumerate(tfRecord):
        print(index)
        if index == maxIterations:
            break
        
        grundTruthJson.append(parseTFRecordToJSONWithPool(tfRecordPart))
    return grundTruthJson

def addGrundTruthToEvaluator(evaluator, grundTruthJson):
    for oneImage in grundTruthJson:
        if oneImage['groundtruth_boxes'] == []:
            oneImage['groundtruth_boxes'] = np.empty((0,4))
        oneImage['groundtruth_boxes'] = np.array(oneImage['groundtruth_boxes'])
        oneImage['groundtruth_classes'] = np.array(oneImage['groundtruth_classes'])
        evaluator.add_single_ground_truth_image_info(image_id=oneImage['filename'], groundtruth_dict=oneImage)

def addDetectedImageInfoToEvaluator(evaluator, imageJsonPath):
    with open(imageJsonPath) as jsonFile:
        imageDetected = json.load(jsonFile)
        print('number of analysed images: ', imageDetected)
        for imagePredict in imageDetected:
            if imagePredict['detection_boxes'] == []:
                imagePredict['detection_boxes'] = np.empty((0,4))
            imagePredict['detection_boxes'] = np.array(imagePredict['detection_boxes'])
            #depending on framework you have to add here +1
            imagePredict['detection_classes'] = np.array(imagePredict['detection_classes'])
            imagePredict['detection_scores'] = np.array(imagePredict['detection_scores'])
            evaluator.add_single_detected_image_info(image_id=imagePredict['fileName'], detections_dict=imagePredict)

def parseTFRecordToJSONWithPool(inputString):
    with Pool(1) as p:
        return p.apply(parseTFRecordToJSON, (inputString,))

def parseTFRecordToJSON(inputString):
    tfSession = tf.Session(config=config)
    decoded = tfExampleDecoder.decode(inputString)
    executedTensors = tfSession.run(decoded)
    returnStats = {}
    returnStats['groundtruth_boxes'] = np.array(executedTensors['groundtruth_boxes'])
    returnStats['groundtruth_classes'] = np.array(executedTensors['groundtruth_classes'])
    returnStats['filename'] = str(executedTensors['filename'])
    tfSession.close()
    print(returnStats)
    return returnStats

def createEvaluator(LabelMapPath):
    categories = label_map_util.create_categories_from_labelmap(LabelMapPath)
    evaluator = coco_evaluation.CocoDetectionEvaluator(categories=categories)
    return evaluator

def openTFRecord(path):
    tfRecordReader = tf.python_io.tf_record_iterator(path)
    return tfRecordReader


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, 
            np.float64)):
            return float(obj)
        elif isinstance(obj,(np.ndarray,)): #### This is the fix
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    tf.app.run()
