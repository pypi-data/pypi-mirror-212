#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   types.py
@Author  :   Raighne.Weng
@Version :   1.1.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Types for Datature API resources.
'''

from enum import Enum
from dataclasses import dataclass


@dataclass
class ProjectMetadata:
    """Project metadata.

    :param name: The name of the project.
    """

    name: str


@dataclass
class AnnotationMetadata:
    """Annotation metadata.

    :param asset_id: The unique ID of the asset.
    :param tag: The tag class name of the annotation.
    :param bound_type: The bound type of the annotation (rectangle or polygon).
    :param bound: The bound coordinates of the annotation in [[x1, y1], [x2, y2], ... , [xn, yn]] format.
    """

    asset_id: str
    tag: str
    bound_type: str
    bound: list


@dataclass
class AnnotationExportOptions:
    """Annotation exported options.

    :param split_ratio: The ratio used to split the data into training and validation sets.
    :param shuffle: Boolean to indicate whether the exported annotations should be shuffled. Defaults to True.
    :param seed: The number used to initialize a pseudorandom number generator to randomize the annotation shuffling.
    :param normalized: Boolean to indicate whether the bound coordinates of the exported annotations should be normalized.
        Defaults to True.

    """

    split_ratio: int
    seed: int
    normalized: bool = True
    shuffle: bool = True


@dataclass
class Pagination:
    """Pagination Params.

    :param page: An optional cursor to specify pagination if there are multiple pages of results.
    :param limit: A limit on the number of objects to be returned in a page. Defaults to 10.
        If the length of the function call results exceeds the limit, the results will be broken into multiple pages.
    """

    page: str
    limit: int = 10


@dataclass
class AssetMetadata:
    """Asset Metadata.

    :param status: The annotation status of the asset (annotated, review, completed, tofix, none).
    :param custom_metadata: A dictionary containing any key-value pairs.
    """

    status: str
    custom_metadata: object


class AnnotationFormat(Enum):
    """Annotation CSV Format.

    Bounding Box Options:
        coco
        csv_fourcorner
        csv_widthheight
        pascal_voc
        yolo_darknet
        yolo_keras_pytorch
        createml
        tfrecord

    Polygon Options:
        polygon_single
        polygon_coco
    """

    COCO = "coco"
    CSV_FOURCORNER = "csv_fourcorner"
    CSV_WIDTHHEIGHT = "csv_widthheight"
    PASCAL_VOC = "pascal_voc"
    YOLO_DARKNET = "yolo_darknet"
    YOLO_KERAS_PYTORCH = "yolo_keras_pytorch"
    CREATEML = "createml"
    TFRECORD = "tfrecord"
    POLYGON_COCO = "polygon_coco"
    POLYGON_SINGLE = "polygon_single"


@dataclass
class DeploymentMetadata:
    """Deployment Settings Metadata.

    :param name: The name of the deployment instance.
    :param model_id: The ID of the exported artifact to be deployed.
    :param num_of_instances: Number of deployment instances to spawn. Defaults to 1.
    """

    name: str
    model_id: str
    num_of_instances: int = 1


@dataclass
class Accelerator:
    """The hardware accelerator to be used for the training.

    :param name: The name of the GPU to be used for the training (GPU_T4, GPU_V100, GPU_P100, GPU_K80).
    :param count: The number of GPUs to be used for the training. More GPUs will use up more compute minutes. Defaults to 1.
    """

    name: str
    count: int = 1


@dataclass
class Checkpoint:
    """The checkpoint metric to be used for the training.

    :param strategy: The checkpointing strategy to be used for the training.

        Checkpoint Strategies:
            STRAT_EVERY_N_EPOCH: Checkpoints are saved at intervals of n epochs.
            STRAT_ALWAYS_SAVE_LATEST: The final checkpoint is always saved.
            STRAT_LOWEST_VALIDATION_LOSS: The checkpoint with the lowest validation loss is saved.
            STRAT_HIGHEST_ACCURACY: The checkpoint with the highest accuracy is saved.

    :param metric: The checkpointing metric to be used for training. Note that metrics starting with "Loss"
        are only applicable when the strategy is set to "STRAT_LOWEST_VALIDATION_LOSS", and metrics starting with
        "DetectionBoxes" are only applicable when the strategy is set to "STRAT_HIGHEST_ACCURACY".

        Loss:
            Loss/total_loss
            Loss/regularization_loss
            Loss/classification_loss
            Loss/localization_loss

        Precision:
            DetectionBoxes_Precision/mAP
            DetectionBoxes_Precision/mAP@.50IOU
            DetectionBoxes_Precision/mAP@.75IOU
            DetectionBoxes_Precision/mAP (small)
            DetectionBoxes_Precision/mAP (medium)
            DetectionBoxes_Precision/mAP (large)

        Recall:
            DetectionBoxes_Recall/AR@1
            DetectionBoxes_Recall/AR@10
            DetectionBoxes_Recall/AR@100
            DetectionBoxes_Recall/AR@100 (small)
            DetectionBoxes_Recall/AR@100 (medium)
            DetectionBoxes_Recall/AR@100 (large)

    :param evaluation_interval: The step interval for checkpoint evaluation during training. Defaults to 1.
    """

    strategy: str
    metric: str
    evaluation_interval: int = 1


@dataclass
class Limit:
    """The limit configuration for the training.

    :param metric: The limit metric for the training.

        Limit Metrics:
            LIM_MINUTE: Limits the training to a maximum number of minutes before it is killed.
            LIM_EPOCHS: Limits the training to a maximum number of epochs before it is killed.
            LIM_NONE: No limit will be set for the training.

    :param value: The limit value for the training. This value will not be used if the limit metric is "LIM_NONE".
        Defaults to 1.
    """

    metric: str
    value: int = 1


@dataclass
class RunSetupMetadata:
    """The settings to start training.

    :param accelerator: The hardware accelerator to be used for the training.
    :param checkpoint: The checkpoint metric to be used for the training.
    :param limit: The limit configuration for the training.
    :param preview: Boolean to indicate whether preview is enabled for the training. Defaults to True.
    """

    accelerator: Accelerator
    checkpoint: Checkpoint
    limit: Limit
    preview: bool = True


@dataclass
class FlowMetadata:
    """Workflow Metadata.

    :param title: The title of the workflow.
    """

    title: str
