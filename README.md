# event-planned-story-gen
Story Generation code using Event Planning as an intermediate step.

Folder Structure:
```
event-story-generation/
├── data/
│   ├── raw/                    # Raw story datasets
│   ├── processed/              # Processed event data
│   └── graphs/                 # Saved event graphs
├── src/
│   ├── event_extraction/       # Event extraction modules
│   ├── event_planning/         # Event sequence generation (NOT IMPLEMENTED)
│   ├── graph_construction/     # Event graph building
│   ├── story_generation/       # Story generation from events (NOT IMPLEMENTED)
│   └── utils/                  # Utility functions
├── notebooks/                  # Jupyter notebooks for experimentation
├── config/                     # Configuration files
├── requirements.txt
└── README.md
```