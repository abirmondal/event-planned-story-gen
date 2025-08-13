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
    "neg",  # Negation modifier (e.g., "not")
    "prt",  # Phrasal verb particle (e.g., "give up")
]

# Event tags for agents, used to identify the doer of the action.
agent_tags = [
    "agent",  # Agent of the action [usually the doer in passive constructions] (e.g., "The teacher" in "The teacher teaches the student.")
]

# Event tags for objects, used to identify the direct object of the action.
comp_tags = [
    "dobj",  # Direct object (e.g., "I see the dog." - "the dog" is the dobj of "see")
    "acomp", # Adjectival complement (e.g., "She is happy." - "happy" is the acomp of "is")
    "ccomp", # Clausal complement with internal subject (e.g., "I think that he is right." - "that he is right" is the ccomp of "think")
    "xcomp"  # Clausal complement with external subject (e.g., "I want to go." - "to go" is the xcomp of "want")
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