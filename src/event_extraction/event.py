"""
# event.py

This module defines the Event class, which represents an event with a trigger and associated information.
"""

class Event:
    """
    This class represents an event of a sentence.

    An event consists of a trigger (the main event word) and additional information such as modifiers,
    agents, and components. The event information is stored in a dictionary with the following structure:
    ```python
    {
        "trigger": List of triggers associated with the event,
        "modifiers": List of modifiers that describe the event,
        "agents": List of agents involved in the event,
        "comps": List of components related to the event
    }
    ```

    Attributes:
        trigger (str): The main event trigger (e.g., "marriage", "birthday").
        event_info (dict): A dictionary containing additional information about the event.
                           It can include "trigger", "modifiers", "agents", and "comps".
    """
    def __init__(self, trigger: str, event_info: dict = None):
        """
        Initializes an Event instance.

        Args:
            trigger (str): The main event trigger (e.g., "marriage", "birthday").
            event_info (dict, optional): A dictionary containing additional information about the event.
                    - "trigger": List of triggers associated with the event.
                    - "modifiers": List of modifiers that describe the event.
                    - "agents": List of agents involved in the event.
                    - "comps": List of components related to the event.
        """
        self.trigger = trigger
        self.event_info = event_info if event_info is not None else {
            "trigger": [],
            "modifiers": [],
            "agents": [],
            "comps": [],
        }

    def __str__(self):
        """
        Returns a string representation of the Event instance, including the trigger and all components.

        Returns:
            str: A string representation of the Event instance.
        """
        all_components = []  # Collect all components from the event_info dictionary
        for one in self.event_info.values():
            all_components.extend(one)  # Flatten the list of components

        # Sort components in ascending order based on indices
        all_components.sort(key=lambda x: x[1], reverse=False)

        # Remove extra spaces in the components
        all_components = [comp[0].strip()
                          for comp in all_components if comp[0].strip()]

        # Convert all components into one string
        all_components_string = ' '.join(all_components)

        return all_components_string

    def __repr__(self):
        """
        Returns a string representation of the Event instance for debugging purposes.

        Returns:
            str: A string representation of the Event instance.
        """
        return str(self.__dict__)
