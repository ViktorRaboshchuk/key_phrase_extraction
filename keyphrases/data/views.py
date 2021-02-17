from django.shortcuts import render, redirect
from data.forms import TextForm
from data.models import Text, KeyPhrases
from collections import Counter
import pke
import ast
from data.utils import get_keywords, wikipedia_check


def text_save(request):
    if 'save' in request.POST:
        form = TextForm(request.POST)
        if form.is_valid():
            form.save()
            form = TextForm()
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
        key_list = ast.literal_eval(key_list.phrases)
        for phrase in key_list:
            all_phrases.append(phrase)
    counted_phrases = Counter(all_phrases).most_common(10)
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
        context = get_keywords(text)
        if 'wikipedia_pages' in request.POST:
            wiki_urls, disambiguation = wikipedia_check(kp_obj)
            context['wiki_urls'] = wiki_urls
            context['disambiguation'] = disambiguation

        return render(request, 'data/text_page.html', context=context)

    elif request.method == 'GET':
        context = get_keywords(text)
        return render(request, 'data/text_page.html', context=context)

    elif 'keyphrases_extract' in request.POST:
        extractor = pke.unsupervised.TopicRank()
        extractor.load_document(input=text.text_area)
        extractor.candidate_selection()
        extractor.candidate_weighting()
        keyphrases = extractor.get_n_best(n=10)
        key_phrases = [x[0] for x in keyphrases]
        ph, created = KeyPhrases.objects.get_or_create(
            key=text,
            phrases=key_phrases)
        context = {'text': text, 'key_phrases': key_phrases}
        return render(request, 'data/text_page.html', context=context)
    else:
        context = get_keywords(text)
        return render(request, 'data/text_page.html', context=context)

