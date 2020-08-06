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


# This script loads the generated images and merge them to one TFRecord file.
# This script depends on the tutorial from https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/using_your_own_dataset.md


import tensorflow as tf
import glob
import cv2
import io
import xml.etree.ElementTree as ET

from object_detection.utils import dataset_util

basePath = 'D:/Projekte/autonomous-driving/'
savePath = basePath + 'working/training/'
loadPath = basePath + 'working/images'
loadTestPath = basePath + 'working/imagesTest'

labelMap = {b'blue': 1, b'yellow': 2, b'orange': 3}


def createOneRecord(image, xml, label_map):

    height = int(xml.find('size').find('height').text)
    width = int(xml.find('size').find('width').text)
    filename = xml.find('path').text.encode('utf-8')
    encoded_image_data = image
    image_format = b'png'

    xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = [] # List of normalized right x coordinates in bounding box
                # (1 per box)
    ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = [] # List of normalized bottom y coordinates in bounding box
                # (1 per box)
    classes_text = [] # List of string class name of bounding box (1 per box)
    classes = [] # List of integer class id of bounding box (1 per box)

    for box in xml.findall('object'):
        xmins.append(int(box.find('bndbox').find('xmin').text)/ width)
        xmaxs.append(int(box.find('bndbox').find('xmax').text) / width)
        ymins.append(int(box.find('bndbox').find('ymin').text) / height)
        ymaxs.append(int(box.find('bndbox').find('ymax').text) / height)
        class_text = box.find('name').text.encode('utf-8')
        classes_text.append(class_text)
        classes.append(label_map[class_text])


    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_image_data),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example

def getImages(path):
    fileList = glob.glob(path + '/*.png')
    for file in fileList:
        image = cv2.imread(file)
        image = cv2.imencode('.png', image)[1].tostring()
        xml = ET.parse(file.replace('.png', '.xml')).getroot()
        yield image, xml

def generateLabelMap(labelMap):
    labelString = ""
    for label in labelMap:
        labelString += 'item {\n'
        labelString += '  id: ' + str(labelMap[label]) + '\n'
        labelString += "  name: '" + label.decode('utf-8') + "'\n"
        labelString += '}\n'
        labelString += '\n'
    return labelString



def main(_):

    #label
    labelString = generateLabelMap(labelMap)
    with open(savePath +'mscoco_label_map.pbtxt','w') as labelFile:
        labelFile.write(labelString)

    #train
    images = getImages(loadPath)
    writer = tf.python_io.TFRecordWriter(savePath + 'mscoco_train.record')
    for (image, xml) in images:
        imageRecord = createOneRecord(image, xml, labelMap)
        writer.write(imageRecord.SerializeToString())
        print('.',end='', flush=True)
    writer.close()

    #test
    images = getImages(loadTestPath)
    writer = tf.python_io.TFRecordWriter(savePath + 'mscoco_val.record')
    for (image, xml) in images:
        imageRecord = createOneRecord(image, xml, labelMap)
        writer.write(imageRecord.SerializeToString())
        print('.',end='', flush=True)
    writer.close()

    print('generate recording ready')


if __name__ == '__main__':
  tf.app.run()
