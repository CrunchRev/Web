"""
2024, Written by the CrunchRev Authors

Module description: controls filtering
"""

from better_profanity import profanity

class TextFilter:
    def __init__(self):
        profanity.load_censor_words()

        return None
    
    def censor(self, sentence):
        return profanity.censor(sentence, "#")