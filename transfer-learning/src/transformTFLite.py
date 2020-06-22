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
import os

#Enter here the version number of the checkpoint this is the number behind model.ckpt-
checkpointVersion = 102954

basePath = 'D:/Projekte/autonomous-driving/'
modelBasePath = 'transfer-learning/model/'
model = 'ssdlite_mobilenet_v2_coco_2018_05_09/'
checkpointPath = basePath + 'working/model/' + model
tfLiteModel = 'working/tfLite/' + model

sys.argv.append('--trained_checkpoint_prefix=' + checkpointPath + 'model.ckpt-' + str(checkpointVersion))
sys.argv.append('--pipeline_config_path='+ basePath + modelBasePath + model +'pipeline.config') 
sys.argv.append('--output_directory='+ basePath + tfLiteModel) 
sys.argv.append('--add_postprocessing_op=true')



command = "tflite_convert "
# command += "--inference_type=QUANTIZED_UINT8 "
command += "--graph_def_file="+ basePath + tfLiteModel + "tflite_graph.pb "
command += "--output_file="+ basePath + tfLiteModel + "detect.tflite "
command += "--output_format=TFLITE --input_shapes=1,300,300,3 "
command += "--input_arrays=normalized_input_image_tensor "
command += "--output_arrays=TFLite_Detection_PostProcess,TFLite_Detection_PostProcess:1,TFLite_Detection_PostProcess:2,TFLite_Detection_PostProcess:3 "
command += "--change_concat_input_ranges=false "
command += "--allow_custom_ops "
command += "--mean_values=128 "
command += "--std_dev_values=128 "
#set default ranges is not a good idea
# this is only needen if the model is not quantified
# command += "--default_ranges_min=-6 "
# command += "--default_ranges_max=6"

print('')
print('please run this command after you executed this script')
print('')
print(command)
print('')
print('')
print('')

import tensorflow as tf
from object_detection import export_tflite_ssd_graph 

# create frozen tf grath, .pb and .pbtxt
tf.app.run(main = export_tflite_ssd_graph.main)