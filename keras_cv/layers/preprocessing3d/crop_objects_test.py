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
import numpy as np
import tensorflow as tf

from keras_cv.layers.preprocessing3d import base_augmentation_layer_3d
from keras_cv.layers.preprocessing3d.crop_objects import CropObjects

POINT_CLOUDS = base_augmentation_layer_3d.POINT_CLOUDS
BOUNDING_BOXES = base_augmentation_layer_3d.BOUNDING_BOXES
OBJECT_POINT_CLOUDS = base_augmentation_layer_3d.OBJECT_POINT_CLOUDS
OBJECT_BOUNDING_BOXES = base_augmentation_layer_3d.OBJECT_BOUNDING_BOXES


class CorpObjectsTest(tf.test.TestCase):
    def test_augment_point_clouds_and_bounding_boxes(self):
        add_layer = CropObjects(
            label_index=1,
            min_points_per_bounding_boxes=1,
            max_points_per_bounding_boxes=2,
        )
        point_clouds = np.array(
            [[[0, 1, 2, 3, 4], [10, 1, 2, 3, 4], [0, -1, 2, 3, 4], [100, 100, 2, 3, 4]]]
            * 2
        ).astype("float32")
        bounding_boxes = np.array(
            [
                [
                    [0, 0, 0, 4, 4, 4, 0, 1],
                    [10, 1, 2, 2, 2, 2, 0, 1],
                    [20, 20, 20, 1, 1, 1, 0, 1],
                ]
            ]
            * 2
        ).astype("float32")
        inputs = {POINT_CLOUDS: point_clouds, BOUNDING_BOXES: bounding_boxes}
        outputs = add_layer(inputs)
        object_point_clouds = np.array(
            [[[[0, 1, 2, 3, 4], [0, -1, 2, 3, 4]], [[10, 1, 2, 3, 4], [0, 0, 0, 0, 0]]]]
            * 2
        ).astype("float32")
        object_bounding_boxes = np.array(
            [[[0, 0, 0, 4, 4, 4, 0, 1], [10, 1, 2, 2, 2, 2, 0, 1]]] * 2
        ).astype("float32")
        self.assertAllClose(inputs[POINT_CLOUDS], outputs[POINT_CLOUDS])
        self.assertAllClose(inputs[BOUNDING_BOXES], outputs[BOUNDING_BOXES])
        self.assertAllClose(outputs[OBJECT_POINT_CLOUDS], object_point_clouds)
        self.assertAllClose(outputs[OBJECT_BOUNDING_BOXES], object_bounding_boxes)

    def test_augment_batch_point_clouds_and_bounding_boxes(self):
        add_layer = CropObjects(
            label_index=1,
            min_points_per_bounding_boxes=1,
            max_points_per_bounding_boxes=2,
        )
        point_clouds = np.array(
            [
                [
                    [
                        [0, 1, 2, 3, 4],
                        [10, 1, 2, 3, 4],
                        [0, -1, 2, 3, 4],
                        [100, 100, 2, 3, 4],
                    ]
                ]
                * 2
            ]
            * 3
        ).astype("float32")
        bounding_boxes = np.array(
            [
                [
                    [
                        [0, 0, 0, 4, 4, 4, 0, 1],
                        [10, 1, 2, 2, 2, 2, 0, 1],
                        [20, 20, 20, 1, 1, 1, 0, 1],
                    ]
                ]
                * 2
            ]
            * 3
        ).astype("float32")
        inputs = {POINT_CLOUDS: point_clouds, BOUNDING_BOXES: bounding_boxes}
        outputs = add_layer(inputs)
        object_point_clouds = np.array(
            [
                [
                    [
                        [[0, 1, 2, 3, 4], [0, -1, 2, 3, 4]],
                        [[10, 1, 2, 3, 4], [0, 0, 0, 0, 0]],
                    ]
                ]
                * 2
            ]
            * 3
        ).astype("float32")
        object_bounding_boxes = np.array(
            [[[[0, 0, 0, 4, 4, 4, 0, 1], [10, 1, 2, 2, 2, 2, 0, 1]]] * 2] * 3
        ).astype("float32")
        self.assertAllClose(inputs[POINT_CLOUDS], outputs[POINT_CLOUDS])
        self.assertAllClose(inputs[BOUNDING_BOXES], outputs[BOUNDING_BOXES])
        self.assertAllClose(outputs[OBJECT_POINT_CLOUDS], object_point_clouds)
        self.assertAllClose(outputs[OBJECT_BOUNDING_BOXES], object_bounding_boxes)
