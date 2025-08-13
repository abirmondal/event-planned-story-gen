"""
# config/dir.py

This module defines directory paths used in the project.
"""

from pathlib import Path

# Define the base directory as the parent directory of this file's parent
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory for data files
DATA_DIR = BASE_DIR / "data"
# Directory for ROCStories processed data
ROCSTORIES_DIR = DATA_DIR / "processed" / "rocstories_name_replaced"
# Directory for processed data files
PROCESSED_DATA_DIR = DATA_DIR / "processed"
# Directory for raw data files
RAW_DATA_DIR = DATA_DIR / "raw"
# Directory for graph data files
GRAPH_DATA_DIR = DATA_DIR / "graph"

def update_directories(base_dir: str):
    """
    Update the directory paths based on the current environment.

    Args:
        base_dir (str): The base directory path.
    """
    global BASE_DIR, DATA_DIR, ROCSTORIES_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR, GRAPH_DATA_DIR
    BASE_DIR = Path(base_dir).resolve()
    DATA_DIR = BASE_DIR / "data"
    ROCSTORIES_DIR = DATA_DIR / "processed" / "rocstories_name_replaced"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    RAW_DATA_DIR = DATA_DIR / "raw"
    GRAPH_DATA_DIR = DATA_DIR / "graph"
