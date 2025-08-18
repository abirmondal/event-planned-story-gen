"""
# event_build.py

This module provides functionality to build a directed event graph from event sequences in a DataFrame.
Each node represents an event with a frequency attribute, and each edge represents a transition between events.
"""

import pickle
import pandas as pd
import networkx as nx
from typing import Union
from tqdm.auto import tqdm
import config.event_special_tokens as event_special_tokens
import config.dir as dir

class EventGraphBuilder:
    """
    A class for building a directed event graph from event sequences in a DataFrame.
    Each node is an event with a frequency attribute.
    Each edge represents a transition and can be weighted (e.g., by co-occurrence count).
    """

    def __init__(self, graph_type: str = 'DiGraph'):
        """
        Initialize the EventGraphBuilder with an existing NetworkX DiGraph or creates a new one.

        Args:
            graph_type (str): Type of the graph to be created. Default is 'DiGraph'. Other options include 'Graph' for undirected graphs.
        """
        if graph_type not in ['DiGraph', 'Graph']:
            raise ValueError(f"Invalid graph type: {graph_type}. Choose 'DiGraph' or 'Graph'.")
        
        self.graph = nx.DiGraph() if graph_type == 'DiGraph' else nx.Graph()

    def build_graph(self, df: pd.DataFrame, event_col: str = None) -> None:
        """
        Forms the directed event graph from the DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame. Must contain one column with event sequences.
            event_col (str): Name of the column containing event sequences. If None, uses the first column.
        """
        # If the Graph is not empty, through error
        if self.graph.number_of_nodes() > 0:
            raise ValueError("Graph is already built. Please create a new instance to build a new graph.")
        
        # If event_col is not specified, use the first column
        if event_col is None:
            event_col = df.columns[0]

        for seq in tqdm(df[event_col], desc="Building Event Graph"):
            # Split events and strip whitespace
            events = [e.strip() for e in seq.split(
                event_special_tokens.EVENT_SEPERATOR)]

            # Remove [EVENT_s] from the start of the first event, if present
            if events and events[0].startswith(event_special_tokens.EVENT_START):
                events[0] = events[0].replace(
                    event_special_tokens.EVENT_START, '', 1).strip()
            # Remove [EVENT_e] from the end of the last event, if present
            if events and events[-1].endswith(event_special_tokens.EVENT_END):
                events[-1] = events[-1].replace(
                    event_special_tokens.EVENT_END, '', 1).strip()

            # Remove any empty events (after stripping)
            events = [e for e in events if e]

            # Skip if there are no actual events left
            if not events:
                continue

            for i, event in enumerate(events):
                if event not in self.graph:
                    # Add the event node with initial frequency 0
                    self.graph.add_node(event, frequency=0)
                # Increment the frequency of the event node
                self.graph.nodes[event]['frequency'] += 1

                if i > 0:
                    prev_event = events[i - 1]
                    if self.graph.has_edge(prev_event, event):
                        # Increment the weight of the edge if it already exists
                        self.graph[prev_event][event]['weight'] += 1
                    else:
                        # Add a new edge with weight 1
                        self.graph.add_edge(prev_event, event, weight=1)

    def get_graph(self) -> Union[nx.DiGraph, nx.Graph]:
        """
        Returns the constructed graph.

        Returns:
            nx.DiGraph or nx.Graph: The directed or undirected graph containing events as nodes and transitions as edges.
        """
        if self.graph.number_of_nodes() == 0:
            raise ValueError("Graph is empty. Please build the graph first.")
        return self.graph

    def save_graph_pickle(self, filename: str) -> None:
        """
        Saves the constructed graph to a pickle file using networkx.write_gpickle.

        Args:
            filename (str): The output file name using which the graph will be saved.
        """
        if not filename.endswith('.gpickle'):
            filename += '.gpickle'
        filepath = dir.GRAPH_DIR / filename
        # Ensure the directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if self.graph.number_of_nodes() == 0:
            raise ValueError("Graph is empty. Please build the graph before saving.")
        
        # Save the graph to a pickle file
        with open(filepath, 'wb') as f:
            pickle.dump(self.graph, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Graph saved to {filepath}.")

    def load_graph_pickle(self, filename: str) -> nx.DiGraph:
        """
        Loads a graph from a pickle file using networkx.read_gpickle.

        Args:
            filename (str): The input file name from which the graph will be loaded.
        """
        filepath = dir.GRAPH_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Graph file {filepath} does not exist.")
        if not filepath.suffix == '.gpickle':
            raise ValueError("File must be a .gpickle file.")
        
        # Load the graph from the pickle file
        with open(filepath, 'rb') as f:
            self.graph = pickle.load(f)
        print(f"Graph loaded from {filepath}.")
        return self.graph
    
    def save_graph_gexf(self, filename: str) -> None:
        """
        Saves the constructed graph to a GEXF file using networkx.write_gexf.
        This is useful for visualization in tools like Gephi.

        Args:
            filename (str): The output file name using which the graph will be saved.
        """
        if not filename.endswith('.gexf'):
            filename += '.gexf'
        filepath = dir.GRAPH_DIR / filename
        # Ensure the directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if self.graph.number_of_nodes() == 0:
            raise ValueError("Graph is empty. Please build the graph before saving.")

        nx.write_gexf(self.graph, filepath)
        print(f"Graph saved to {filepath}.")

    def load_graph_gexf(self, filename: str) -> nx.DiGraph:
        """
        Loads a graph from a GEXF file using networkx.read_gexf.

        Args:
            filename (str): The input file name from which the graph will be loaded.
        """
        filepath = dir.GRAPH_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Graph file {filepath} does not exist.")
        if not filepath.suffix == '.gexf':
            raise ValueError("File must be a .gexf file.")
        self.graph = nx.read_gexf(filepath)
        print(f"Graph loaded from {filepath}.")
        return self.graph
