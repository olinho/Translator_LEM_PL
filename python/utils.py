
import itertools
import operator
import re

from functools import reduce


def firstLetterFromSentencesToUpper(sentences):
    return [sent[0].upper() + sent[1:] for sent in sentences]


# does a permutation lists
def listsToSentences(lists):
    sets_of_words = list(itertools.product(*lists))
    sentences = [" ".join(list(sets_of_words[i])) for i in range(0, sets_of_words.__len__() - 1)]
    sentences = firstLetterFromSentencesToUpper(sentences)
    return sentences


def saveLemkosSentences(sentences):
    lem_sentences_file = open("data/lemkos_sentences.txt", 'w', encoding="UTF-8")
    for sent in sentences:
        lem_sentences_file.write(sent + "\n")


def savePolishSentences(sentences):
    pl_sentences_file = open("data/polish_sentences.txt", 'w', encoding="UTF-8")
    for sent in sentences:
        pl_sentences_file.write(sent + "\n")

# l_lem is list of lists of words (noun, verb, etc.)
def createAndSaveToFileSentences(l_lem, l_pl):
    lem_sentences = listsToSentences(l_lem)
    pl_sentences = listsToSentences(l_pl)
    saveLemkosSentences(lem_sentences)
    savePolishSentences(pl_sentences)

def flatten(l: []):
    return reduce(operator.concat,l)

def unnest_list(l: []):
    while True:
        l = flatten(l)
        try:
            if len(l) > 0:
                continue
        except Exception:
            return l
        return l

def get_words(sentence):
    return [word.lower() for word in re.findall(r'\w+', sentence)]

def format_text(text: str):
    pattern = re.compile(r'\s+')
    formatted = re.sub(pattern, ' ', text)
    return formatted

def filter_none(l: []):
    return list(filter(lambda x: x!=None, l))
