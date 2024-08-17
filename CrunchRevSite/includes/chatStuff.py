"""
2024, Written by the CrunchRev Authors

Module description: controls filtering
"""

from better_profanity import profanity

class TextFilter:
    def __init__(self):
        profanity.load_censor_words(whitelist_words=["fuck", "f3ck"])
        profanity.add_censor_words([
            "пиздец", "п1зд3ц", "п1здец", "пизд3ц", 
            "ебать", "3бать", "eбать", "еб@ть",
            "сука", "с_ка", "су_ка", "сук@",
            "блядь", "6лядь", "бля_дь", "бл@дь",
            "хуй", "хyй", "х_й", "ху1"
            "neonazi", "ne0nazi", "neonaz1", "n3onaz1",
            "n30naz1", "dogshit", "dogsh1t", "d0gshit",
            "d0gsh1t"
        ])

        return None
    
    def censor(self, sentence):
        return profanity.censor(sentence, "#")