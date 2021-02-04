import wikipedia
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from data.forms import TextForm
from data.models import Text, KeyPhrases
import RAKE
from django.template.defaulttags import register
from collections import Counter

from data.utils import get_keywords, wikipedia_check


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def text_save(request):
    form = TextForm()
    key_phrases = None
    if 'save' in request.POST:
        form = TextForm(request.POST)
        if form.is_valid():
            form.save()
            form = TextForm()
        redirect('/')
    else:
        form = TextForm()
    return render(request, 'data/text_save.html', {'form': form})


def all_texts(request):
    texts = Text.objects.all()
    ordered_texts = texts.order_by('-time')
    context = {'all_texts': ordered_texts}
    return render(request, 'data/all_texts.html', context=context)


def top_keywords(request):
    all_phrases = []
    all_keywords_list = KeyPhrases.objects.all()
    for key_list in all_keywords_list:
        for phrase in key_list.phrases:
            all_phrases.append(phrase)
    counted_phrases = Counter(all_phrases).most_common(20)
    context = {'all_keywords': counted_phrases}

    if 'wikipedia_pages' in request.POST:
        wiki_urls, disambiguation = wikipedia_check(counted_phrases)
        context['wiki_urls'] = wiki_urls
        context['disambiguation'] = disambiguation

    return render(request, 'data/top_keywords.html', context=context)


def text_page(request, pk):
    text = Text.objects.get(id=pk)
    kp_obj = KeyPhrases.objects.filter(key=text)

    if request.method == 'POST' and kp_obj.exists():
        context = get_keywords(request, text)
        if 'wikipedia_pages' in request.POST:
            wiki_urls, disambiguation = wikipedia_check(kp_obj)
            context['wiki_urls'] = wiki_urls
            context['disambiguation'] = disambiguation

        return render(request, 'data/text_page.html', context=context)

    elif request.method == 'GET':
        context = get_keywords(request, text)
        return render(request, 'data/text_page.html', context=context)
    else:
        stop_dir = 'data/stop.txt'
        rake_object = RAKE.Rake(stop_dir)
        keywords = rake_object.run(text.text_area)[:10]
        key_phrases = [x[0] for x in keywords]
        ph, created = KeyPhrases.objects.get_or_create(
            key=text,
            phrases=key_phrases)
        context = {'text': text, 'key_phrases': key_phrases}
        return render(request, 'data/text_page.html', context=context)


def wikipedia_page(request):
    #
    # for phrase in kp_obj[0].phrases:
    #     try:
    #         wiki_search = wikipedia.summary(phrase, sentences=2,chars=20, auto_suggest=False)
    #         print(phrase)
    #         wiki_page = wikipedia.page(phrase, auto_suggest=False)
    #         print(wiki_page.url)
    #     except wikipedia.exceptions.PageError:
    #         continue
    #     except wikipedia.exceptions.DisambiguationError as e:
    #         print(e.options)

    ny = wikipedia.page("Vodka")
    print(ny.title)
    if request.method == 'GET':
        wiki_url = ny.url
        print(wiki_url)
        return HttpResponseRedirect(wiki_url)
