# Copyright 2022 The KerasCV Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tensorflow as tf

from keras_cv.layers.preprocessing3d import base_augmentation_layer_3d
from keras_cv.ops.point_cloud import wrap_angle_radians

POINT_CLOUDS = base_augmentation_layer_3d.POINT_CLOUDS
BOUNDING_BOXES = base_augmentation_layer_3d.BOUNDING_BOXES


class GlobalRandomFlippingY(base_augmentation_layer_3d.BaseAugmentationLayer3D):
    """A preprocessing layer which flips point clouds and bounding boxes along with respect to the Y axis during training.

    This layer will flip the whole scene with respect to the Y axis.
    During inference time, the output will be identical to input. Call the layer with `training=True` to flip the input.

    Input shape:
      point_clouds: 3D (multi frames) float32 Tensor with shape
        [num of frames, num of points, num of point features].
        The first 5 features are [x, y, z, class, range].
      bounding_boxes: 3D (multi frames) float32 Tensor with shape
        [num of frames, num of boxes, num of box features].
        The first 7 features are [x, y, z, dx, dy, dz, phi].

    Output shape:
      A tuple of two Tensors (point_clouds, bounding_boxes) with the same shape as input Tensors.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_random_transformation(self, **kwargs):
        return None

    def augment_point_clouds_bounding_boxes(
        self, point_clouds, bounding_boxes, transformation, **kwargs
    ):
        del transformation

        point_clouds_y = -point_clouds[..., 1:2]

        point_clouds = tf.concat(
            [point_clouds[..., 0:1], point_clouds_y, point_clouds[..., 2:]], axis=-1
        )

        bounding_boxes_y = -bounding_boxes[..., 1:2]
        bounding_boxes_heading = wrap_angle_radians(-bounding_boxes[..., 6:7])
        bounding_boxes = tf.concat(
            [
                bounding_boxes[..., 0:1],
                bounding_boxes_y,
                bounding_boxes[..., 2:6],
                bounding_boxes_heading,
                bounding_boxes[..., 7:],
            ],
            axis=-1,
        )

        return (point_clouds, bounding_boxes)