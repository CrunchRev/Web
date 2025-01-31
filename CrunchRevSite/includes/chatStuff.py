"""
2024 - 2025, Written by the CrunchRev Authors

Module description: controls filtering
"""

from better_profanity import profanity

class TextFilter:
    def __init__(self):
        profanity.load_censor_words()
        profanity.add_censor_words([
            "пиздец", "п1зд3ц", "п1здец", "пизд3ц", "пиздец", "пиздюк", "пиздеть",
            "пиздец", "пиздос", "пиздёт", "пиздяк", "пиздливый", "пиздёныш",
            "ебать", "3бать", "eбать", "еб@ть", "ебаный", "еб@ный", "ебануть",
            "ебануться", "ебаненький", "ебаная", "ебливый", "ебучий", "ебливый",
            "ебанутый", "ебаный", "еб@нутость", "ебл@нь", "е6ать", "3б@ть",
            "сука", "с_ка", "су_ка", "сук@", "с_ука", "сук@", "сукин", "сукин@",
            "с@ка", "с_ка", "с_у_ка", "сyка", "сy_ка", "с_у_ка", "сyк@",
            "сука", "сук@", "суkа", "сука", "сyка",
            "блядь", "6лядь", "бля_дь", "бл@дь", "бляха", "блядюга", "блядище",
            "блядочка", "бл@дь", "блядьё", "бля_дя", "бл@дь", "бля@", "бл@к@",
            "бл@ч", "бля_ха", "бл@дище", "бл@дос",
            "хуй", "хyй", "х_й", "ху1", "хуево", "хуевый", "хуевая", "хуйню",
            "хуйня", "хуёв", "ху!й", "хy!й", "хyй0", "хуй0", "хуй1", "хуй_ня",
            "ху1", "ху@", "ху1ня", "ху!ня", "хуйо",
            "пидор", "пидорас", "пидорок", "пидораска", "пидр", "пидр0", "пид0рас",
            "п!дорас", "п1д0рас", "пид0р", "п!д0р", "п!д0рок", "пид0р0к", "пидорас",
            "пид0р", "п1д0р", "пидорасик", "пид0р0к",
            "долбаёб", "долб@ёб", "д0лб@ёб", "д0лб0ёб", "д0лб@ёб", "д0лбаёб",
            "долбаёб", "долбаёб", "д0лб@ёб", "д0лб@ёб", "д0лб0ёб", "долб0ёб",
            "мразь", "мразь", "мразь", "мразь", "мраз@ь", "мраз0", "мраз1",
            "мразь0", "мразь", "мразя", "мразина", "мраза", "мразот", "мразотина",
            "гандон", "ганд0н", "г@нд0н", "ганд0н", "ганд0н", "г@нд0н",
            "ганд0н", "г@нд0н", "г0нд0н", "ганд@н", "г@нд0н",
            "сучка", "с_чка", "с_чка", "суч@ка", "сучка", "сyчка", "суч0ка",
            "сучк@", "сучка", "сучёнок", "сучка", "сyч0к@",
            "neonazi", "ne0nazi", "neonaz1", "n3onaz1", "n30naz1", "neonazi",
            "dogshit", "dogsh1t", "d0gshit", "d0gsh1t", "doggyshit", "d0gsh!t",
            "sh1t", "p00p", "p00py",
            "д0гш1т", "пердун", "пуки", "пердеж", "пук", "плакс", "плакса",
            "долбоёб", "ссанина", "мразот", "жопа", "задница", "зад", "выродок",
            "свинья", "мразотина", "сучка", "гнилое мясо", "гнилой", "урод",
            "дебил", "тупой", "тупица", "идиот", "дебил", "салага", "подонок",
            "тварь", "отстой", "петушня", "тупорылый", "говядина", "пердак",
            "засранец", "пиздобол", "всё как всегда", "вот такая вот хуйня",
            "тупица", "херня", "пиздотень", "вот тебе и", "пиздострадатель",
            "долбежка", "гандом", "гондобой", "гандон", "мудошар", "падла",
            "пиздозавр", "пиздобратия", "педрил", "жопотёрка", "пукалка",
            "ебало", "салоед", "пидорский", "пидорасик", "козлятина", "гавноед",
            "блядьё", "хер", "фекалии", "гнилотина"
        ])

        return None
    
    def censor(self, sentence):
        return profanity.censor(sentence, "#")