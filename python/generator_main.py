import json


import utils
import lemko_json_file_worker
import linguistic_converter
from psql_worker import PsqlWorker

db = PsqlWorker()

ling_conv = linguistic_converter.LinguisticConverterPl()

def do_next_word(word: str):

    details = db.get_word_details(word)[0]

    node_decl = {}
    node_conj = {}
    node_rest = {}
    node = {}
    gramm_part_of_speech = details['grammatical_part_of_speech']

    node_rest = {"tlumaczenie": "", "czesc_mowy": ""}
    node_rest['tlumaczenie'] = utils.format_text(details['polish_translation'])
    node_rest['czesc_mowy'] = details['grammatical_part_of_speech']
    node_word = details['base_form']
    if gramm_part_of_speech == 0:
        node_rest['rodzaj'] = details['grammatical_gender']

    node[node_word] = node_rest

    if gramm_part_of_speech == 0:
        decl = db.get_noun_declination(word)
        node_decl = {"deklinacja": {0: {}, 1: {}}}
        for el in decl:
            node_decl['deklinacja'][el['grammatical_number']][el['grammatical_case']] = el['word']

    if gramm_part_of_speech == 1:
        conj = db.get_conjugation(word)
        node_conj = {"koniugacja": {0: {}, 1: {}, 2: {}}}
        for el in conj:
            node_conj['koniugacja'][el['grammatical_tense']][el['grammatical_person']] = el['word']

    if gramm_part_of_speech == 2:
        decl = db.get_adjective_declination(word)
        node_decl = {"deklinacja": {'meski': {'rowny': {0: {}, 1: {}}, 'wyzszy': {0: {}, 1: {}}, 'najwyzszy': {0: {}, 1: {}}},
                                    'zenski': {'rowny': {0: {}, 1: {}}, 'wyzszy': {0: {}, 1: {}}, 'najwyzszy': {0: {}, 1: {}}},
                                    'nijaki': {'rowny': {0: {}, 1: {}}, 'wyzszy': {0: {}, 1: {}}, 'najwyzszy': {0: {}, 1: {}}}
                                    }}
        rodzaj = ''
        for el in decl:
            gramm_gender = el['grammatical_gender']
            if gramm_gender == 0:
                rodzaj = 'meski'
            elif gramm_gender == 1:
                rodzaj = 'zenski'
            elif gramm_gender == 2:
                rodzaj = 'nijaki'
            else:
                rodzaj = 'nijaki'

            gramm_comparison = el['grammatical_comparison']
            if gramm_comparison == 0:
                stopien = 'rowny'
            elif gramm_comparison == 1:
                stopien = 'wyzszy'
            elif gramm_comparison == 2:
                stopien = 'najwyzszy'
            else:
                stopien = 'rowny'

            node_decl['deklinacja'][rodzaj][stopien][el['grammatical_number']][el['grammatical_case']] = el['word']


    node[node_word].update(node_decl)
    node[node_word].update(node_conj)

    print(node)
    with open("data/lemko_words.json", "r", encoding="utf8") as file:
        lemko_dict = json.load(file)
    lemko_dict.update(node)

    with open('data/lemko_words.json', 'wb') as file:
        file.write(json.dumps(lemko_dict, indent=2, sort_keys=True, ensure_ascii=False).encode('utf8'))

def show_details(word: str):
    details = db.get_word_details(word)[0]
    print(details)
    part_of_speech = details['grammatical_part_of_speech']
    if part_of_speech == 0:
        decl = db.get_noun_declination(word)
        print(decl)
    elif part_of_speech == 1:
        conj = db.get_conjugation(word)
        print(conj)
    elif part_of_speech == 2:
        decl = db.get_adjective_declination(word)
        print(decl)

def add_next_words_to_json(limit=10):
    words = db.get_new_words(lemko_json_file_worker.get_lemko_words(), limit=limit)
    for word in words:
        print('Word ' + word)
        try:
            do_next_word(word)
        except Exception as e:
            print(e)
    print(words)

def fill_the_json(words):
    known_words = lemko_json_file_worker.get_lemko_words()
    unknown_words = [word for word in words if word not in known_words]
    for word in unknown_words:
        print('Word ' + word)
        try:
            do_next_word(word)
        except Exception as e:
            print(e)

# get words from sentence and add unknown to lemko_words.json
def update_lemko_words_json_for_sentence(sent):
    base_forms_in_sent = get_base_forms(sent)
    filtered_base_forms = utils.filter_none(base_forms_in_sent)
    fill_the_json(filtered_base_forms)

# get list of words from sentence in base forms
def get_base_forms(sent: str):
    words_in_sent = utils.get_words(sent)
    return [db.get_base_form_for_word(word) for word in words_in_sent]

def has_sentence_unknown_word(sent: str):
    base_forms = get_base_forms(sent)
    if None in base_forms:
        return True
    else:
        return False


# add_next_words_to_json()
word = "простий"
# sent = db.get_sentence_with_word(word)
sent = "Дуб стоіт коло дорогы"
# sentences = db.get_sentences_with_word(word)
for s in [sent]:
    print(s)
    print(get_base_forms(s))
    print(has_sentence_unknown_word(s))
update_lemko_words_json_for_sentence(sent)
update_lemko_words_json_for_sentence('білий')
# lemko_json_file_worker.get_grammar_division_for_sentence(sent)