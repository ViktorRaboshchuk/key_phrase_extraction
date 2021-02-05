import wikipedia
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from data.models import KeyPhrases


def get_keywords(text):
    try:
        db_key_phrases = KeyPhrases.objects.get(key=text)
        context = {'text': text, 'key_phrases': db_key_phrases.phrases}
    except ObjectDoesNotExist:
        db_key_phrases = []
        context = {'text': text, 'key_phrases': db_key_phrases}

    return context


def wikipedia_check(kp_obj):
    disambiguation = {}
    wiki_urls = {}
    if isinstance(kp_obj, QuerySet):
        for phrase in kp_obj[0].phrases:
            try:
                wiki_summary = wikipedia.summary(phrase, sentences=1, chars=10, auto_suggest=False)
                wiki_page = wikipedia.page(phrase, auto_suggest=True)
                wiki_urls[phrase] = wiki_page.url
            except wikipedia.exceptions.DisambiguationError:
                disambiguation[phrase] = 'This keyword refers to multiple pages!:)'
            except wikipedia.exceptions.PageError:
                wiki_urls[phrase] = ''
                continue
    elif isinstance(kp_obj, list):
        for phrase, cnt in kp_obj:
            try:
                wiki_summary = wikipedia.summary(phrase, sentences=2, chars=20, auto_suggest=False)
                wiki_page = wikipedia.page(phrase, auto_suggest=True)
                wiki_urls[phrase] = wiki_page.url
            except wikipedia.exceptions.DisambiguationError:
                disambiguation[phrase] = 'This keyword refers to multiple pages!'
            except wikipedia.exceptions.PageError:
                wiki_urls[phrase] = ''
                continue
            except KeyError:
                continue

    return wiki_urls, disambiguation
