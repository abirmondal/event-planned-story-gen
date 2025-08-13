"""
# config/dir.py

This module defines directory paths used in the project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# This line finds and loads the key-value pairs from your .env file
load_dotenv()

# Get BASE_DIR from the environment; default to the current directory if not found.
# The value is immediately converted to a Path object for consistency.
BASE_DIR = Path(os.environ.get("BASE_DIR", Path.cwd()))

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
