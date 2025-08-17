# config/event_tags.py

# This file contains the event tags used in the event-planned story generation project.
# Event tags are used to identify and categorize different types of events in the text.

# Event tags for Subjects, used to identify the subject of a sentence.
subject_tags = [
    "csubj",     # Clausal subject (Example: "I think that he is right.", "I" is the csubj of "think")
    "csubjpass", # Clausal subject, passive (Example: "It is believed that he is right.", "It" is the csubjpass of "is believed")
    "nsubj",     # Nominal subject (Example: "The cat sleeps.", "The cat" is the nsubj of "sleeps")
    "nsubjpass"  # Nominal subject, passive (Example: "The book was read by the student.", "The book" is the nsubjpass of "was read")
]

# Event tags for trigger verb or verb phrases.
verb_phrase_tags = [
    "neg",  # Negation modifier (e.g., “not”)
    "prt",  # Phrasal verb particle (e.g., “give up”)
    'ROOT'  # The main verb (root of the sentence)
]

# Event tag for the main verb or root of the sentence, used to identify the primary action.
trigger_tags = [
    "ROOT",  # The main verb (root of the sentence)
]

# Event tags for modifiers, used to identify negation and phrasal verb particles.
modifier_tags = [
    "neg",     # Negation modifier (e.g., "not")
    "prt",     # Phrasal verb particle (e.g., "give up")
    # Extra context for modifier identification
    "advmod",  # Adverbial modifier (e.g., "quickly")
    "amod",    # Adjectival modifier (e.g., "happy")
]

# Event tags for agents, used to identify the doer of the action.
agent_tags = [
    "agent",  # Agent of the action [usually the doer in passive constructions] (e.g., "The teacher" in "The teacher teaches the student.")
]

agent_tags.extend(subject_tags)  # Include subject tags as agents (Extra context for agent identification)

# Event tags for objects, used to identify the direct object of the action.
comp_tags = [
    "dobj",     # Direct object (e.g., "I see the dog." - "the dog" is the dobj of "see")
    "acomp",    # Adjectival complement (e.g., "She is happy." - "happy" is the acomp of "is")
    "ccomp",    # Clausal complement with internal subject (e.g., "I think that he is right." - "that he is right" is the ccomp of "think")
    "xcomp",    # Clausal complement with external subject (e.g., "I want to go." - "to go" is the xcomp of "want")
    # (Following tags are extra context for component identification)
    "oprd",     # Object predicate (e.g., "She made him happy." - "happy" is the oprd of "made")
    "attr",     # Attribute (e.g., "The sky is blue." - "blue" is the attr of "is")
    "pobj",     # Object of a preposition (e.g., "She sat on the chair." - "chair" is the pobj of "on"
    "dative",   # Dative case (e.g., "I gave him a book." - "him" is the dative of "gave")
    "npadvmod", # Noun phrase adverbial modifier (e.g., "He left early." - "early" is the npadvmod of "left")
]

# Event tags to specify POS tags for verbs.
verb_pos = [
    "VB",  # Verb, base form
    "VBD", # Verb, past tense
    "VBG", # Verb, gerund or present participle
    "VBN", # Verb, past participle
    "VBP", # Verb, non-3rd person singular present
    "VBZ"  # Verb, 3rd person singular present
]