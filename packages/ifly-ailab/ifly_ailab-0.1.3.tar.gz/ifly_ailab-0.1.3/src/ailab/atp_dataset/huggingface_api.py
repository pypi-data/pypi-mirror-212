import os
from typing import (Dict,  Union)
from datasets import (load_dataset,load_from_disk)
from datasets import inspect
from datasets import Dataset, DatasetDict, IterableDataset, IterableDatasetDict

class HFDatasetAPI :
    def __init__(self) -> None:
        pass

    def load(dataset_name: str,) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        hf_dataset = load_dataset(dataset_name)
        return hf_dataset
        
    def load_disk(dataset:str, dataset_format:str)-> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        if os.path.isfile(dataset):
            hf_dataset = load_dataset(path=dataset_format, data_files=dataset)
        elif os.path.isdir(dataset):
            hf_dataset = load_from_disk(dataset)
        return hf_dataset
    
    def list() -> str :
        dataset = inspect.list_datasets()
        return dataset
    
    def train_test_split(dataset : Dataset, test_size:float) :
        return dataset.train_test_split(test_size=test_size)