"""
# event_extract.py

This module provides the EventExtractor class, which is responsible for extracting events from text using a spaCy NLP model.
"""

import re
import spacy
import pandas as pd
from tqdm.notebook import tqdm
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

    def extract_events_from_story_df(self, df: pd.DataFrame, df_type: str, is_save: bool = True) -> None:
        """
        Extract events from a DataFrame containing story texts.

        :param df: A pandas DataFrame with a column 'target' containing story texts.
        :param df_type: The type of DataFrame (e.g., 'train', 'test', 'val').
        :param is_save: Whether to save the extracted events to a file.
        """
        for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Extracting events"):
            story = row['target']
            events = self.extract_events_from_story(story)
            events_string = event_special_tokens.EVENT_START + " " + \
                (" " + event_special_tokens.EVENT_SEPERATOR + " ").join(str(event) for event in events) + \
                " " + event_special_tokens.EVENT_END
            df.at[index, 'events'] = events_string

        if is_save:
            output_path = f"{ROCSTORIES_DIR}/{df_type}_event.source_new.txt"
            df['events'].to_csv(output_path, index=False, header=False)
            print(f"Events extracted and saved to {output_path}")
