"""
event_evals.py

This module provides utility functions for evaluating events.
"""

import pickle
import numpy as np
import pandas as pd
import evaluate
from transformers import AutoTokenizer
from joblib import Parallel, delayed
from tqdm.auto import tqdm
from config.dir import EVENT_GRAPH_MAP_DIR

rouge = evaluate.load("rouge")
bleu = evaluate.load("bleu")


def jaccard_similarity_for_text(text1, text2) -> float:
    """
    Calculate the Jaccard similarity between two texts.

    Args:
        text1 (str): The first text.
        text2 (str): The second text.

    Returns:
        float: The Jaccard similarity between the two texts.
    """
    words1 = set(text1.split())
    words2 = set(text2.split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if len(union) > 0 else 0.0


def get_best_event_from_graph_nodes(test_event: str, events_list: list, return_score: bool = False) -> dict:
    """
    Find the event from the graph with the highest Jaccard similarity to the test event.

    Args:
        test_event (str): The event to compare against.
        events_list (list): A list of events to evaluate.
        return_score (bool): Whether to return the similarity score along with the event.

    Returns:
        
    """
    similarities = []
    for event in events_list:
        similarity = jaccard_similarity_for_text(test_event, event)
        similarities.append((event, similarity))

    max_similarity_event = max(similarities, key=lambda x: x[1])
    if return_score:
        return {"event": max_similarity_event[0], "score": max_similarity_event[1]}
    return {"event": max_similarity_event[0]}

def events_map_to_best_graph_events(events: list, events_list: list, return_score: bool = False, cpu_parallel: bool = False, cpu_n_jobs: int = -1) -> list:
    """
    Map a list of events to the closest events in the graph using Jaccard similarity.

    Args:
        events (list): A list of events to map.
        events_list (list): A list of events from the graph for comparison.
        return_score (bool): Whether to return the similarity score along with the event.
        cpu_parallel (bool): Whether to use parallel processing on CPU.
        cpu_n_jobs (int): Number of CPU jobs to use for parallel processing. Default is -1 (use all available cores).

    Returns:
        list: A list of mapped events from the graph.
    """
    if cpu_parallel:
        graph_maps = Parallel(n_jobs=cpu_n_jobs, backend="multiprocessing")(
            delayed(get_best_event_from_graph_nodes)(event, events_list, return_score)
            for event in tqdm(events, desc="Mapping events to graph events")
        )
    else:
        graph_maps = [get_best_event_from_graph_nodes(event, events_list, return_score) for event in tqdm(
            events, desc="Mapping events to graph events")]
    
    return graph_maps


def calculate_metrics_for_events(tokenizer: AutoTokenizer, metrics_prefix: str = "", use_graph_events: bool = False, event_list: list = None,  cpu_parallel: bool = False, cpu_n_jobs: int = -1, save_graph_map: bool = False, save_graph_map_file_name: str = "") -> callable:
    """
    Create a function to compute evaluation metrics for a batch of predictions and labels.

    Args:
        tokenizer: The tokenizer used to decode token IDs to text.
        metrics_prefix (str): A prefix to add to the metric names. Default is an empty string.
        use_graph_events (bool): Whether to map predicted events to the closest event in the graph.
        event_list (list): A list of events from the graph for comparison. Required if use_graph_events is True.
        cpu_parallel (bool): Whether to use parallel processing on CPU.
        cpu_n_jobs (int): Number of CPU jobs to use for parallel processing. Default is -1 (use all available cores).
        save_graph_map (bool): Whether to save the graph mapping results to a file.
        save_graph_map_file_name (str): The name of the file to save the graph mapping results. Default is an empty string, which will use "graph_mapped_events.csv".

    Returns:
        function: A function that computes evaluation metrics for a batch of predictions and labels.
    """
    if save_graph_map_file_name == "" and save_graph_map:
        save_graph_map_file_name = "graph_mapped_events.csv"

    if use_graph_events and event_list is None:
        raise ValueError("event_list must be provided when use_graph_events is True")

    if metrics_prefix:
        metrics_prefix = metrics_prefix + "/"

    def computer_metrics(pred_events):
        """
        Compute evaluation metrics for a batch of predictions and labels.

        Args:
            pred_events: A tuple containing predicted events and true labels.

        Returns:
            dict: A dictionary containing evaluation metrics.
            - rouge1 (float): ROUGE-1 score.
            - rouge2 (float): ROUGE-2 score.
            - rougeL (float): ROUGE-L score.
            - rougeLsum (float): ROUGE-Lsum score.
            - bleu (float): BLEU score.
            - gen_len (float): Average length of generated events.
        """
        prediction, labels = pred_events

        # Decode the precicted events
        decoded_preds = tokenizer.batch_decode(
            prediction, skip_special_tokens=True)

        # Replace -100 in the labels as we can't decode them
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)

        # Decode the true events
        decoded_labels = tokenizer.batch_decode(
            labels, skip_special_tokens=True)

        if use_graph_events:
            # Map the decoded predictions to the closest event in the graph
            graph_maps = events_map_to_best_graph_events(decoded_preds, event_list, return_score=True, cpu_parallel=cpu_parallel, cpu_n_jobs=cpu_n_jobs)

            # Save the graph mapping results to a file if required
            if save_graph_map:
                data = {
                    "original_event": decoded_preds,
                    "mapped_event": [graph_map["event"] for graph_map in graph_maps],
                    "similarity_score": [graph_map["score"] for graph_map in graph_maps]
                }
                df = pd.DataFrame(data)
                df.to_csv(EVENT_GRAPH_MAP_DIR / save_graph_map_file_name, index=False)
                # Delete the dataframe to free up memory
                del df

            # Replace the decoded predictions with the mapped events
            decoded_preds = [graph_map["event"] for graph_map in graph_maps]
                

        # Calculate ROUGE scores
        result = rouge.compute(predictions=decoded_preds,
                               references=decoded_labels, use_stemmer=True)
        result = {f"{metrics_prefix}{key}": value for key,
                  value in result.items()}

        # Calculate BLEU score
        result[f"{metrics_prefix}bleu"] = bleu.compute(
            predictions=decoded_preds, references=[[label] for label in decoded_labels])["bleu"]

        # Calculate the average length of the generated events
        result[f"{metrics_prefix}gen_len"] = np.mean([np.count_nonzero(pred != tokenizer.pad_token_id) for pred in prediction])

        return result

    return computer_metrics
