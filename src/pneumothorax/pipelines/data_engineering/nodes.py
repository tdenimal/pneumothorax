import pandas as pd
import numpy as np

from typing import List,Dict,Tuple
from PIL import Image


def array_to_img(array: np.ndarray, 
                size: Tuple[int, int] = (256,256)) -> Image:
    """Convert np.ndarray (pixel array) to PIL.Image and resizes eventually

    Args:
        array (np.ndarray): the input pixel array
        size (Tuple[int, int], optional): (width,height) of returned PIL.Image. Defaults to (256,256).

    Returns:
        Image: PIL.Image as output
    """
    return Image.fromarray(array).resize(size=(size[0], size[1]))



def preprocess_dicom(dicom: Dict) -> List:
    """Extract data from dicom.

    Args:
        dicom (Dict): dcm files ( PartitionedDataSet )

    Returns:
        List: [pandas.DataFrame (csv file), Dict of PIL.IMage ( PartitionedDataSet )
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
