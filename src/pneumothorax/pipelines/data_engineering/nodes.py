import pandas as pd
import numpy as np

from typing import List,Dict,Tuple

from kedro.io import PartitionedDataSet, MemoryDataSet
from PIL import Image


def array_to_img(array: np.ndarray, 
                size: Tuple[int, int] = (256,256)) -> Image:
    return Image.fromarray(array).resize(size=(size[0], size[1]))



def preprocess_dicom(dicom: Dict) -> List:
    """Extract data from dicom.

        Args:
            dicom: Source data.
        Returns:
            Preprocessed data.

    """

    #Init data with first dict item
    imgs = {}

    partition_id, partition_load_func = dicom.popitem()
    partition_data = partition_load_func()

    csv = partition_data[0]
    imgs[partition_id] = array_to_img(partition_data[1])
    
    #Loop on dict to extract img and csv data
    for partition_id, partition_load_func in dicom.items():
        partition_data = partition_load_func()

        imgs[partition_id] = array_to_img(partition_data[1])

        csv = pd.concat(
            [csv, partition_data[0]], ignore_index=True, sort=True
        )

    return [csv,imgs]
