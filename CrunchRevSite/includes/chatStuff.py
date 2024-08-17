"""
2024, Written by the CrunchRev Authors

Module description: controls filtering
"""

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
            if word in normalized_sentence:
                censored_word = '#' * len(word)
                sentence = sentence.lower().replace(word, censored_word)
                normalized_sentence = self.normalize_text(sentence)
        return sentence