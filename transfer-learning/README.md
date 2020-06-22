# transfer-learning

through the training data and pre trained networks these are adapted to our needs

In this project we use a copy of the Object detection API from https://github.com/tensorflow/models/blob/master/research/object_detection. You can find the copy of the code in the folder "object_detection" and "nets"

# usage after installation

We have to do a view steps to get a TFlite model

* generateTFRecord -> this transforms the images from the image-generator to one .record file
* trainModel -> uses the .record file and trains the model, this creates saves checkpoints
* transformTFLite -> uses a checkpoint and the config to create a TFLite model.

# object_detection

In src the object_detection and nets form slim is from https://github.com/tensorflow/models form the folder models-master/research i deleted the test folders because of size



# installation

The complete installation is in the version control. So you have to do nothing if you clone it.

After installation of environment.yml we have to do a view more things. The installation tutorial is at https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md

## set python path
```
set PYTHONPATH=D:\Projekte\autonomous-driving\transfer-learning\src
```
## generate protos

protoc --python_out=. .\object_detection\protos\anchor_generator.proto .\object_detection\protos\argmax_matcher.proto .\object_detection\protos\bipartite_matcher.proto .\object_detection\protos\box_coder.proto .\object_detection\protos\box_predictor.proto .\object_detection\protos\eval.proto .\object_detection\protos\faster_rcnn.proto .\object_detection\protos\faster_rcnn_box_coder.proto .\object_detection\protos\grid_anchor_generator.proto .\object_detection\protos\hyperparams.proto .\object_detection\protos\image_resizer.proto .\object_detection\protos\input_reader.proto .\object_detection\protos\losses.proto .\object_detection\protos\matcher.proto .\object_detection\protos\mean_stddev_box_coder.proto .\object_detection\protos\model.proto .\object_detection\protos\optimizer.proto .\object_detection\protos\pipeline.proto .\object_detection\protos\post_processing.proto .\object_detection\protos\preprocessor.proto .\object_detection\protos\region_similarity_calculator.proto .\object_detection\protos\square_box_coder.proto .\object_detection\protos\ssd.proto .\object_detection\protos\ssd_anchor_generator.proto .\object_detection\protos\string_int_label_map.proto .\object_detection\protos\train.proto .\object_detection\protos\keypoint_box_coder.proto .\object_detection\protos\multiscale_anchor_generator.proto .\object_detection\protos\graph_rewriter.proto .\object_detection\protos\calibration.proto .\object_detection\protos\flexible_grid_anchor_generator.proto .\object_detection\protos\target_assigner.proto


# show tensorboard during running training

tensorboard --logdir=D:\Projekte\autonomous-driving\working\model