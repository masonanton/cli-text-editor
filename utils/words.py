from english_words import get_english_words_set
from wordfreq import word_frequency

def relevance(word):
    return word_frequency(word, 'en')

english_words = sorted(
    get_english_words_set(['web2'], lower=True),
    key=relevance,
    reverse=True
)
