"""
# data_for_train.py

This module defines the DataForTrain class, which extends BaseDataClassDF for dataset preparation tasks specific to training data.
"""

from datasets import Dataset
from src.dataset_prep.base_data_class import BaseDataClassHF
from config.dir import ROCSTORIES_DIR

class DataForTrain(BaseDataClassHF):
    """
    Class for preparing training data.

    This class extends BaseDataClass to handle dataset preparation tasks specifically for training data.
    """

    def __init__(
            self,
            source_filename_suffix: str = None,
            target_filename_suffix: str = None,
            event_filename_suffix: str = None,
            data_types: list = ['train', 'test', 'val'],
            data_cols: list = ['source', 'target'],
            ):
        """
        Initializes the DataForTrain class with specific file suffixes.

        Args:
            source_filename_suffix (str): Suffix for the source filename (default: None).
            target_filename_suffix (str): Suffix for the target filename (default: None).
            event_filename_suffix (str): Suffix for the event filename (default: None).
        """
        super().__init__(
            source_filename_suffix=source_filename_suffix,
            target_filename_suffix=target_filename_suffix,
            event_filename_suffix=event_filename_suffix,
            data_types=data_types,
            data_cols=data_cols,
        )

    def get_data_for_lc_to_event(self) -> Dataset:
        """
        Prepares the dataset for event generation from leading context.

        This method loads the data and returns Hugging Face Dataset object with only source and event columns.

        Returns:
            Dataset: A Hugging Face Dataset object containing the prepared data.
        """
        self.load_data(event_read=True)

        # Filter the dataset to include only the 'source' and 'event' columns
        training_dataset = {
            data_type: self.dataset[data_type].select_columns(['source', 'event'])
            for data_type in self.data_types
        }

        return training_dataset
