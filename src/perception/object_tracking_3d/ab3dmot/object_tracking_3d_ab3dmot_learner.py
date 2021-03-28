# Copyright 2020-2021 OpenDR European Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import torch
from typing import List, Optional
from engine.learners import Learner
from engine.datasets import DatasetIterator, ExternalDataset, MappedDatasetIterator
from engine.target import BoundingBox3DList, TrackingBoundingBox3D, TrackingBoundingBox3DList
from perception.object_tracking_3d.ab3dmot.algorithm.ab3dmot import AB3DMOT
from perception.object_tracking_3d.ab3dmot.logger import Logger


class ObjectTracking3DAb3dmotLearner(Learner):
    def __init__(
        self,
        device="cpu",
        max_staleness=2,
        min_updates=3,
        state_dimensions=10,  # x, y, z, rotation_y, l, w, h, speed_x, speed_z, angular_speed
        measurment_dimensions=7,  # x, y, z, rotation_y, l, w, h
        state_transition_matrix=None,
        measurement_function_matrix=None,
        covariance_matrix=None,
        process_uncertainty_matrix=None,
        iou_threshold=0.01,
    ):
        # Pass the shared parameters on super's constructor so they can get initialized as class attributes
        super(ObjectTracking3DAb3dmotLearner, self).__init__(
            device=device,
        )

        self.max_staleness = max_staleness
        self.min_updates = min_updates
        self.state_dimensions = state_dimensions
        self.measurment_dimensions = measurment_dimensions
        self.state_transition_matrix = state_transition_matrix
        self.measurement_function_matrix = measurement_function_matrix
        self.covariance_matrix = covariance_matrix
        self.process_uncertainty_matrix = process_uncertainty_matrix
        self.iou_threshold = iou_threshold

        self.__create_model()

    def save(self, path):
        pass

    def load(
        self,
        path,
    ):
        pass

    def reset(self):
        self.model.reset()

    def fit(
        self,
        dataset,
        val_dataset=None,
        logging_path=None,
        silent=False,
        verbose=False,
    ):
        pass

    def eval(
        self,
        dataset,
        logging_path=None,
        silent=False,
        verbose=False,
        image_shape=(1224, 370),
        count=None,
    ):

        logger = Logger(silent, verbose, logging_path)

        logger.close()

        return result

    def infer(self, bounding_boxes_3d_list):

        if self.model is None:
            raise ValueError("No model created")

        is_single_input = True

        if isinstance(bounding_boxes_3d_list, BoundingBox3DList):
            bounding_boxes_3d_list = [bounding_boxes_3d_list]
        elif isinstance(bounding_boxes_3d_list, list):
            is_single_input = False
        else:
            return ValueError(
                "bounding_boxes_3d_list should be a BoundingBox3DList or a list of BoundingBox3DList"
            )

        results = []

        for box_list in bounding_boxes_3d_list:
            result = self.model.update(box_list)
            results.append(result)

        if is_single_input:
            results = results[0]

        return results

    def optimize(self):
        pass

    def __create_model(self):

        self.model = AB3DMOT(
            frame=0,
            max_staleness=self.max_staleness,
            min_updates=self.min_updates,
            state_dimensions=self.state_dimensions,
            measurment_dimensions=self.measurment_dimensions,
            state_transition_matrix=self.state_transition_matrix,
            measurement_function_matrix=self.measurement_function_matrix,
            covariance_matrix=self.covariance_matrix,
            process_uncertainty_matrix=self.process_uncertainty_matrix,
            iou_threshold=self.iou_threshold,
        )