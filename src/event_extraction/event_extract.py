"""
# event_extract.py

This module provides the EventExtractor class, which is responsible for extracting events from text using a spaCy NLP model.
"""

import re
import spacy
import pandas as pd
from tqdm.notebook import tqdm
from collections import defaultdict
from config.dir import ROCSTORIES_DIR
import config.event_tags as event_tags
import config.event_special_tokens as event_special_tokens
from src.event_extraction.event import Event

class EventExtractor:
    """
    This class is responsible for extracting events from text using a spaCy NLP model.

    Attributes:
        nlp (spacy.Language): The spaCy NLP model used for processing text.
    """
    def __init__(self, nlp: spacy.Language):
        """
        Initializes an EventExtractor instance.

        :param nlp: The spaCy NLP model to be used for processing text.
        """
        self.nlp = nlp

    def __get_trigger_info(self, doc: spacy.tokens.Doc) -> tuple:
        """
        Extracts the trigger information from the spaCy Doc object.

        :param doc: The spaCy Doc object containing the processed text.

        :return: A tuple containing the trigger text and its index in the document.
        """
        for token in doc:
            if token.dep_ in event_tags.trigger_tags:
                return (token.text, token.i)
        return None

    def __get_args(self, doc: spacy.tokens.Doc, trigger: str) -> tuple:
        """
        Extracts the arguments related to the trigger from the spaCy Doc object.

        :param doc: The spaCy Doc object containing the processed text.
        :param trigger: The trigger word for which to find related arguments.

        :return: A tuple containing lists of modifiers, agents, and components related to the trigger.
        """
        modifiers = []
        agents = []
        comps = []

        for token in doc:
            if token.head.text == trigger:
                if token.dep_ in event_tags.modifier_tags:
                    modifiers.append((token.text, token.i))
                elif token.dep_ in event_tags.agent_tags:
                    agents.append((token.text, token.i))
                elif token.dep_ in event_tags.comp_tags:
                    comps.append((token.text, token.i))

        return modifiers, agents, comps

    def __clear_special_tags_text(self, text: str) -> str:
        """
        Cleans the input text by removing special event tags.

        :param text: The input text to be cleaned.

        :return: The cleaned text with special tags removed.
        """
        for tag in event_special_tokens.CHAR_TAGS:
            text = text.replace(tag, "")
        return text.strip()

    def extract_event_from_text(self, text: str) -> Event:
        """
        Extract event information from the given text using the spaCy NLP model.

        :param text: The input text from which to extract event information.

        :return: An Event instance containing the extracted event information.
        """
        text = self.__clear_special_tags_text(text)

        doc = self.nlp(text)

        trigger_info = self.__get_trigger_info(doc)
        trigger = trigger_info[0] if trigger_info else None

        if trigger is None:
            return None

        modifiers, agents, comps = self.__get_args(doc, trigger)

        event_info = {
            "trigger": [trigger_info],
            "modifiers": modifiers,
            "agents": agents,
            "comps": comps
        }
        return Event(trigger, event_info)

    def extract_events_from_story(self, story: str) -> list:
        """
        Extract events from the given story text.

        :param story: The input story text from which to extract events.

        :return: A list of Event instances extracted from the story.
        """
        story = self.__clear_special_tags_text(story)

        events = []
        # Split by sentence-ending punctuation
        sentences = re.split(r'(?<=[.!?]) +', story)
        sentences = [s.strip() for s in sentences if s.strip()
                     ]  # Remove empty sentences

        docs = self.nlp.pipe(sentences, batch_size=4)

        for doc in docs:
            trigger_info = self.__get_trigger_info(doc)
            if trigger_info:
                trigger = trigger_info[0]
                modifiers, agents, comps = self.__get_args(doc, trigger)

                event_info = {
                    "trigger": [trigger_info],
                    "modifiers": modifiers,
                    "agents": agents,
                    "comps": comps
                }
                events.append(Event(trigger, event_info))
            else:
                # If no trigger is found, we can either skip or log it
                continue

        return events
    
    def __format_events(self, events_list):
        if not events_list:
            return ""  # Return empty string if no events were found for a story
        return (event_special_tokens.EVENT_START + " " +
                (" " + event_special_tokens.EVENT_SEPERATOR + " ").join(str(event) for event in events_list) +
                " " + event_special_tokens.EVENT_END)

    def extract_events_from_story_df(self, df: pd.DataFrame, df_type: str, batch_size: int = 256, is_save: bool = True) -> None:
        """
        Extracts events from a DataFrame by processing all stories in a single, optimized batch.

        :param df: A pandas DataFrame with a column 'target' containing story texts.
        :param df_type: The type of DataFrame (e.g., 'train', 'test', 'val').
        :param is_save: Whether to save the extracted events to a file.
        """
        all_sentences = []
        story_indices = []  # To map each sentence back to its original story index in the DataFrame

        # Flatten all stories into a single list of sentences
        for index, story in df['target'].items():
            story = self.__clear_special_tags_text(story)
            sentences = [s.strip() for s in re.split(
                r'(?<=[.!?]) +', story) if s.strip()]

            # Add the sentences to our master list
            all_sentences.extend(sentences)
            # For each sentence added, store the original story's index
            story_indices.extend([index] * len(sentences))

        
        # Process all sentences at once with nlp.pipe
        # This is the main optimization. A large batch size is key.
        # The tqdm progress bar now tracks the most time-consuming part.
        docs = self.nlp.pipe(all_sentences, batch_size=batch_size)

        # --- Step 3: Reconstruct events and group them by original story ---
        # A dictionary to hold lists of events for each story index
        story_events = defaultdict(list)
        # zip lets us iterate through the processed docs and their original story indices together
        for doc, story_index in tqdm(zip(docs, story_indices), total=len(all_sentences), desc=f"Extracting events from {df_type} data"):
            trigger_info = self.__get_trigger_info(doc)
            if trigger_info:
                trigger = trigger_info[0]
                modifiers, agents, comps = self.__get_args(doc, trigger)

                event_info = {
                    "trigger": [trigger_info],
                    "modifiers": modifiers,
                    "agents": agents,
                    "comps": comps
                }
                # Create the Event object and append it to the correct story's list
                story_events[story_index].append(Event(trigger, event_info))

        # Apply the formatting function to the grouped events
        df['events'] = df.index.map({index: self.__format_events(
            events) for index, events in story_events.items()})

        if is_save:
            output_path = f"{ROCSTORIES_DIR}/{df_type}_event.source_new.txt"
            df['events'].to_csv(output_path, index=False, header=False)
            print(f"Events extracted and saved to {output_path}")
