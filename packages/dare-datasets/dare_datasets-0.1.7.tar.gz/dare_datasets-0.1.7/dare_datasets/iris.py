import typing

import numpy as np  # For train/test split
import pandas as pd  # For reading the iris csv file

from dare_datasets.dataset_abc import Dataset  # The dataset abstract class
from dare_datasets.utils.downloader import \
    get_file_from_gdrive  # Utility to download from gdrive

GDRIVE_URL = "https://drive.google.com/drive/folders/1p38H-5d8LM4VvgaY7nNTCdjj85jram0o?usp=sharing"
DATASET_NAME = "iris"


class Iris(Dataset):
    def __init__(self, cache_dir: typing.Optional[str] = None) -> None:
        super().__init__(DATASET_NAME, cache_dir)

    def get_info(self) -> dict[str, str]:
        return {
            "name": "iris",
            "description": "Three species of iris plants.",
            "url": GDRIVE_URL,
            "original_url": "https://www.kaggle.com/datasets/uciml/iris?resource=download",
            "formats": ["csv"],  # List of available formats
            "dataset_folder": self.dataset_folder if self.data is not None else "NOT_YET_LOADED"
        }

    def _init_data(self):
        # Download the dataset from google drive
        get_file_from_gdrive(url=GDRIVE_URL, cache_dir=self.cache_dir, folder_name=self.dataset_name)

        # Load the csv file
        self.data = pd.read_csv(self.dataset_folder + "iris.csv")

    def get_raw(self) -> pd.DataFrame:
        """ Returns the raw csv file of all the plants"""
        if self.data is None:
            self._init_data()

        return self.data

    def get_processed(self, train_size: float = 0.8) -> dict[str, pd.DataFrame]:
        """
        Returns a dictionary with the train and test splits of the dataset.

        Args:
            train_size: The size of the train split. Defaults to 0.8.
        """
        mask = np.random.rand(len(self.data)) < train_size

        return {
            "train": self.data[mask],
            "test": self.data[~mask]
        }
