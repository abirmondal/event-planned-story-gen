"""
# data_for_train.py

This module defines the DataForTrain class, which extends BaseDataClassDF for dataset preparation tasks specific to training data.
"""

from tqdm.auto import tqdm
from datasets import Dataset, DatasetDict
from src.dataset_prep.base_data_class import BaseDataClassHF
from src.event_extraction.event_extract import event_seq_to_list, event_list_to_seq
from config.event_special_tokens import EVENT_END

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
            data_types: list = ['train', 'val'],
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
        Each event sequence is broken down into individual events, which are concatenated with special tokens.
        For predicting each event, the source is the leading context + the previous events, and the target is the next event.

        Returns:
            Dataset: A Hugging Face Dataset object containing the prepared data.
        """
        self.load_data(event_read=True)

        # Filter the dataset to include only the 'source' and 'event' columns
        dataset_source_event = {
            data_type: self.dataset[data_type].select_columns(['source', 'event'])
            for data_type in self.data_types
        }

        # Convert the dataset to a DatasetDict
        dataset_source_event = DatasetDict(dataset_source_event)
        training_dataset = {}

        # Process each data type to prepare the source and event columns
        for data_type in self.data_types:
            data = dataset_source_event[data_type]
            source = data['source']
            event = data['event']
            sources = []
            events = []

            # Extract individual events from the event sequences
            for i, event_sequence in tqdm(enumerate(event), desc=f"Processing {data_type} data", total=len(event)):
                event_sequence = event_seq_to_list(event_sequence)

                if not event_sequence:
                    continue
                for j, event in enumerate(event_sequence):
                    sources.append(
                        f"{source[i]} {event_list_to_seq(event_sequence[:j], is_end=True, force_start=True)}")
                    events.append(event + " " + EVENT_END)

            training_dataset[data_type] = Dataset.from_dict({
                'source': sources,
                'event': events,
            })

        # Convert the training dataset to a DatasetDict
        training_dataset = DatasetDict(training_dataset)

        return training_dataset
