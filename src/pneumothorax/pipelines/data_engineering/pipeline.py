from kedro.pipeline import node, Pipeline
from pneumothorax.pipelines.data_engineering.nodes import (
    preprocess_dicom,clean_metadata
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=preprocess_dicom,
                inputs="dicom_train",
                outputs=["csv_train","img_train"],
                name="preprocessing_dicom",
            ),
            node(
                func=clean_metadata,
                inputs="csv_train",
                outputs="csv_clean",
                name="clean_metadata",
            ),
        ]
    )