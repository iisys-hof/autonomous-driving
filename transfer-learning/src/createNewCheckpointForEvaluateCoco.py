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
modelBasePath = 'transfer-learning/model/'
model = 'ssd_mobilenet_v2_coco_2018_03_29/'
workingPath = basePath + 'working/evalCoco/' + model


sys.argv.append('--model_dir=' + workingPath)
sys.argv.append('--pipeline_config_path='+ basePath + modelBasePath + model +'pipelineEvalCoco.config')
sys.argv.append('--logtostderr')
sys.argv.append('--run_once=True')


# run tensor flow
import tensorflow as tf
from object_detection import model_main 
tf.app.run(main = model_main.main)