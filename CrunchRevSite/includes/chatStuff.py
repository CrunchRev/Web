"""
2024, Written by the CrunchRev Authors

Module description: controls filtering
"""

from better_profanity import profanity

class TextFilter:
    def __init__(self):
        profanity.load_censor_words()
        profanity.add_censor_words([
            "пиздец", "п1зд3ц", "п1здец", "пизд3ц", 
            "ебать", "3бать", "eбать", "еб@ть",
            "сука", "с_ка", "су_ка", "сук@",
            "блядь", "6лядь", "бля_дь", "бл@дь",
            "хуй", "хyй", "х_й", "ху1"
        ])

        return None
    
    def censor(self, sentence):
        return profanity.censor(sentence, "#")