"""
2024, Written by the CrunchRev Authors

Module description: controls filtering
"""

import re

class TextFilter:
    def __init__(self):
        self.offensive_words = [
            'nigger', 'faggot', 'cunt', 'bitch', 'whore', 'slut', 'tranny', 'retard', 'chink', 'spic', 'kike', 
            'dyke', 'twat', 'asshole', 'motherfucker', 'cocksucker', 'cock', 'dick', 'pussy', 'fucker', 'shit', 
            'nazi', 'kunt', 'spook', 'gook', 'coon'
        ]
    
    def normalize_text(self, text):
        leetspeak_dict = {
            '1': 'i', '2': 'z', '3': 'e', '4': 'a', '5': 's',
            '6': 'g', '7': 't', '8': 'b', '9': 'g', '0': 'o',
            '@': 'a', '$': 's', '!': 'i', '|': 'l', '+': 't',
            '(': 'c', ')': 'c'
        }
        for leet, char in leetspeak_dict.items():
            text = text.replace(leet, char)
        return text

    def censor(self, sentence):
        normalized_sentence = self.normalize_text(sentence.lower())
        for word in self.offensive_words:
            normalized_word = self.normalize_text(word)
            if normalized_word in normalized_sentence:
                censored_word = '#' * len(word)
                sentence = re.sub(r'\b' + re.escape(word) + r'\b', censored_word, sentence, flags=re.IGNORECASE)
                normalized_sentence = self.normalize_text(sentence.lower())
        return sentence