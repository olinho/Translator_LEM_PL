import json
import utils


def get_lemko_dict():
    with open("data/lemko_words.json", "r", encoding="utf8") as file:
        lemko_dict = json.load(file)
    return lemko_dict

def get_lemko_words(dict = get_lemko_dict()):
    return [key.lower() for key in dict.keys()]

def get_nouns(dict = get_lemko_dict()):
    return get_words_from_part_of_speech(0, dict=dict)

def get_verbs(dict = get_lemko_dict()):
    return get_words_from_part_of_speech(1, dict=dict)

def get_adjectives(dict = get_lemko_dict()):
    return get_words_from_part_of_speech(2, dict=dict)

def get_words_from_part_of_speech(part_of_speech, dict = get_lemko_dict()):
    lem_words = get_lemko_words(dict)
    return [word for word in lem_words if dict[word]['czesc_mowy'] == part_of_speech]

def get_grammar_division_for_sentence(sent: str):
    words_in_sent = utils.get_words(sent)
    print(words_in_sent)
    # TODO