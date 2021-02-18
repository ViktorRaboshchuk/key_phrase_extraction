import wikipedia
import ast
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from data.models import KeyPhrases


def get_keywords(text):
    """
    Get saved keyphrases for unique text
    """
    try:
        db_key_phrases = KeyPhrases.objects.get(key=text)
        db_key_phrases = ast.literal_eval(db_key_phrases.phrases)
        context = {'text': text, 'key_phrases': db_key_phrases}
    except ObjectDoesNotExist:
        db_key_phrases = []
        context = {'text': text, 'key_phrases': db_key_phrases}

    return context


def wikipedia_check(kp_obj):
    """
    Search keyphrase on Wikipedia
    """
    disambiguation = {}
    wiki_urls = {}
    array_obj = []
    if isinstance(kp_obj, QuerySet):
        array_obj = ast.literal_eval(kp_obj[0].phrases)
    elif isinstance(kp_obj, list):
        [array_obj.append(i[0]) for i in kp_obj]
    print(array_obj)

    for phrase in array_obj:
        try:
            wiki_summary = wikipedia.summary(phrase, sentences=1, chars=10, auto_suggest=False)
            wiki_page = wikipedia.page(phrase, auto_suggest=True)
            wiki_urls[phrase] = wiki_page.url
        except wikipedia.exceptions.DisambiguationError:
            disambiguation[phrase] = 'This keyword refers to multiple pages!'
        except wikipedia.exceptions.PageError:
            wiki_urls[phrase] = ''
            continue
        print(wiki_urls)
    return wiki_urls, disambiguation
