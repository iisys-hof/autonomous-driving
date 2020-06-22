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

import sys
import threading

basePath = 'D:/Projekte/autonomous-driving/'
cocoDataPath = basePath + 'working/coco/'


sys.argv.append('--logtostderr')
sys.argv.append('--output_dir=' + cocoDataPath + 'TFRecord')
sys.argv.append('--val_image_dir=' + cocoDataPath + 'validationImages')
sys.argv.append('--test_image_dir=' + cocoDataPath + 'testImages')
sys.argv.append('--train_image_dir=' + cocoDataPath + 'trainImages')
sys.argv.append('--val_annotations_file=' + cocoDataPath + 'annotations/instances_val2017.json')
sys.argv.append('--train_annotations_file=' + cocoDataPath + 'annotations/instances_train2017.json')
sys.argv.append('--testdev_annotations_file=' + cocoDataPath + 'annotations/')

# run tensor flow
import tensorflow as tf
from object_detection.dataset_tools import create_coco_tf_record 
tf.app.run(main = create_coco_tf_record.main)
