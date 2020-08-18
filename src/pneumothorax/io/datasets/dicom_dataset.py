from pathlib import PurePosixPath

from typing import Any,Dict

from kedro.io import AbstractDataSet
from kedro.io.core import get_filepath_str, get_protocol_and_path

import fsspec
import numpy as np
import pandas as pd

import pydicom

# PIL is the package from Pillow
from PIL import Image


class DICOMDataSet(AbstractDataSet):
    def __init__(self, filepath: str):
        """Creates a new instance of DICOMDataSet to load / save image data for given filepath.

        Args:
            filepath: The location of the DICOM file to load / save data.
        """
        
        # parse the path and protocol (e.g. file, http, s3, etc.)
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)

    def _load(self) -> (pd.DataFrame,np.ndarray):
        """Loads data from the DICOM file.

        Returns:
            Metadata from the DICOM file as a pandas Dataframe,
            Image data  as a numpy array
        """
        # using get_filepath_str ensures that the protocol and path are appended correctly for different filesystems
        load_path = get_filepath_str(self._filepath, self._protocol)
        with self._fs.open(load_path) as f:
            ds = pydicom.dcmread(f)

            #Convert metadata records to dataframe
            df = pd.DataFrame.from_records([(el.name,el.value) for el in ds if el.name not in ['Pixel Data', 'File Meta Information Version']])
            #Convert row to columns
            df = df.T
            #Set first line as header
            df.columns = df.iloc[0]
            #Delete first line
            df = df.iloc[1:]
            pixel_array = ds.pixel_array
            return (df,pixel_array)
    

    def _save(self, data: np.ndarray) -> None:
        """Saves image data to the specified filepath"""
        return None

    
    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset.
        """
        return dict(
            filepath=self._filepath,
            protocol=self._protocol
        )
