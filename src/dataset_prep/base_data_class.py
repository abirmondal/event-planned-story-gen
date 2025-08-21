"""
# base_data_class.py

This module defines the BaseDataClass, which serves as a base class for dataset preparation tasks.
"""

import os
import pandas as pd
from datasets import Dataset
from config.dir import ROCSTORIES_DIR

class BaseDataClassDF:
    """
    Base class for dataset preparation tasks, using pandas DataFrame.

    This class provides a structure for handling dataset-related operations, including loading and processing data.

    Attributes:
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
        Initializes the BaseDataClassDF with source, target, and event paths.

        Args:
            source_filename_suffix (str): Suffix for the source filename (default: None).
            target_filename_suffix (str): Suffix for the target filename (default: None).
            event_filename_suffix (str): Suffix for the event filename (default: None).
            data_types (list): List of data types to be processed (default: ['train', 'test', 'val']).
            data_cols (list): List of columns to be used in the dataset (default: ['source', 'target']).
        """
        self.source_filename_suffix = source_filename_suffix
        self.target_filename_suffix = target_filename_suffix
        self.event_filename_suffix = event_filename_suffix
        self.data_types = data_types
        self.data_cols = data_cols
        self.data_df = {}

    def load_data(self, show_data_size: bool = False, event_read: bool = False) -> None:
        """
        Loads the dataset from the specified source path.

        This method should be overridden in subclasses to implement specific data loading logic.

        Args:
            show_data_size (bool): If True, prints the size of the loaded data (default: False).
            event_read (bool): Flag indicating whether to read event data (default: False).
        """
        for data_type in self.data_types:
            data = {}
            for col in self.data_cols:
                filepath = f"{ROCSTORIES_DIR}/{data_type}"
                if col == 'source':
                    filepath += self.source_filename_suffix if self.source_filename_suffix else ''
                elif col == 'target':
                    filepath += self.target_filename_suffix if self.target_filename_suffix else ''
                filepath += f".{col}.txt"

                if not os.path.exists(filepath):
                    raise FileNotFoundError(f"File not found: {filepath}")

                with open(filepath, 'r', encoding='utf-8') as f:
                    data[col] = f.read().splitlines()
            
            if event_read:
                filepath = f"{ROCSTORIES_DIR}/{data_type}"
                filepath += self.event_filename_suffix if self.event_filename_suffix else ''
                filepath += f".txt"
                
                if not os.path.exists(filepath):
                    raise FileNotFoundError(f"File not found: {filepath}")
                with open(filepath, 'r', encoding='utf-8') as file:
                    events = file.read().splitlines()

                data['event'] = events

            self.data_df[data_type] = pd.DataFrame(data)
            if show_data_size:
                print(
                    f"Number of rows in {data_type} data: {self.data_df[data_type].shape[0]}")
                
    def get_data_df(self) -> pd.DataFrame:
        """
        Returns the loaded data as a pandas DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the loaded data.
        """
        if not self.data_df:
            raise ValueError("Data not loaded. Please call load_data() first.")
        return self.data_df

class BaseDataClassHF:
    """
    Base class for dataset preparation tasks, using Hugging Face datasets.

    This class provides a structure for handling dataset-related operations, including loading and processing data.
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
        Initializes the BaseDataClassHF with source, target, and event paths.

        Args:
            source_filename_suffix (str): Suffix for the source filename (default: None).
            target_filename_suffix (str): Suffix for the target filename (default: None).
            event_filename_suffix (str): Suffix for the event filename (default: None).
            data_types (list): List of data types to be processed (default: ['train', 'test', 'val']).
            data_cols (list): List of columns to be used in the dataset (default: ['source', 'target']).
        """
        self.source_filename_suffix = source_filename_suffix
        self.target_filename_suffix = target_filename_suffix
        self.event_filename_suffix = event_filename_suffix
        self.data_types = data_types
        self.data_cols = data_cols
        self.dataset = {}

    def load_data(self, show_data_size: bool = False, event_read: bool = False) -> None:
        """
        Loads the dataset from the specified source path.

        This method should be overridden in subclasses to implement specific data loading logic.

        Args:
            show_data_size (bool): If True, prints the size of the loaded data (default: False).
            event_read (bool): Flag indicating whether to read event data (default: False).
        """
        for data_type in self.data_types:
            data = {}
            for col in self.data_cols:
                filepath = f"{ROCSTORIES_DIR}/{data_type}"
                if col == 'source':
                    filepath += self.source_filename_suffix if self.source_filename_suffix else ''
                elif col == 'target':
                    filepath += self.target_filename_suffix if self.target_filename_suffix else ''
                filepath += f".{col}.txt"

                if not os.path.exists(filepath):
                    raise FileNotFoundError(f"File not found: {filepath}")

                with open(filepath, 'r', encoding='utf-8') as f:
                    data[col] = f.read().splitlines()
            
            if event_read:
                filepath = f"{ROCSTORIES_DIR}/{data_type}"
                filepath += self.event_filename_suffix if self.event_filename_suffix else ''
                filepath += f".txt"
                
                if not os.path.exists(filepath):
                    raise FileNotFoundError(f"File not found: {filepath}")
                with open(filepath, 'r', encoding='utf-8') as file:
                    events = file.read().splitlines()

                data['event'] = events

            self.dataset[data_type] = Dataset.from_dict(data)
            if show_data_size:
                print(
                    f"Number of rows in {data_type} data: {self.dataset[data_type].num_rows}")
                
    def get_dataset(self) -> Dataset:
        """
        Returns the loaded dataset as a Hugging Face Dataset.

        Returns:
            Dataset: The Hugging Face Dataset containing the loaded data.
        """
        if not self.dataset:
            raise ValueError("Data not loaded. Please call load_data() first.")
        return self.dataset
