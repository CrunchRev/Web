"""
2024, Written by the CrunchRev Authors

Module description: controls filtering
"""

import re

class TextFilter:
    def __init__(self):
        self.offensive_words = [
            'nigger', 'n1gger', 'nigg3r', 'faggot', 'f4ggot', 'f4g', 'cunt', 'c@nt', 'bitch', 'b1tch', 'b!tch',
            'whore', 'wh0re', 'slut', 'slvt', 'sl*t', 'tranny', 'tr4nny', 'retard', 'r3tard', 'chink', 'ch1nk',
            'spic', 'sp1c', 'kike', 'k1ke', 'dyke', 'd1ke', 'twat', 'tw@t', 'asshole', 'a$$hole', 'assh0le',
            'motherfucker', 'm0therfucker', 'm0th3rfucker', 'motherf*cker', 'cocksucker', 'c0cksucker',
            'c*cksucker', 'cock', 'c0ck', 'c*ck', 'dick', 'd1ck', 'd!ck', 'pussy', 'pu$$y', 'p*ssy', 'fucker',
            'f*cker', 'fu*ker', 'shit', 'sh1t', 'sh!t', 'nazi', 'naz1', 'kunt', 'k*nt', 'spook', 'sp00k',
            'gook', 'g00k', 'coon', 'c00n'
        ]
        
        self.leetspeak_dict = {
            '1': 'i', '2': 'z', '3': 'e', '4': 'a', '5': 's',
            '6': 'g', '7': 't', '8': 'b', '9': 'g', '0': 'o',
            '@': 'a', '$': 's', '!': 'i', '|': 'l', '+': 't',
            '(': 'c', ')': 'c'
        }
    
    def normalize_text(self, text):
        for leet, char in self.leetspeak_dict.items():
            text = text.replace(leet, char)
        return text
    
    def create_pattern(self, word):
        pattern = ''
        for char in word:
            pattern += char + r'\W*'
        return pattern
    
    def censor(self, sentence):
        normalized_text = self.normalize_text(sentence.lower())
        for word in self.offensive_words:
            word_pattern = self.create_pattern(word)
            matches = re.finditer(word_pattern, normalized_text)
            for match in matches:
                start, end = match.span()
                sentence = sentence[:start] + '#' * (end - start) + sentence[end:]
                normalized_text = self.normalize_text(sentence.lower())
        return sentence