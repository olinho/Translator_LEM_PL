from dictionary import Word


class LinguisticConverterPl:
    def __init__(self):
        self.czesc_mowy = {}
        self.rodzaj = {}
        self.przypadek = {}
        self.liczba = {}
        self.osoba = {}
        self.czas = {}
        self.column_names = {}

        self.define_przypadki()
        self.define_liczby()
        self.define_osoby()
        self.define_czasy()
        self.define_rodzaje()
        self.define_czesci_mowy()
        self.define_column_names()

    def get_column_name_for_attribute(self, attr: str):
        return self.column_names[attr]

    def get_liczba(self, word: Word):
        attr_in_raw_form = word.get_number()
        attr_converted = self.liczba[attr_in_raw_form]
        return attr_converted

    def define_column_names(self):
        self.column_names['przypadek'] = 'grammatical_case'
        self.column_names['rodzaj'] = 'T.grammatical_gender'  ## dodane T. tak będziemy nazywać tablelę 'terms' podczas zapytań. Ta kolumna znajduje sie również w drugiej tabeli, dlatego niezbędne jest rozróżnienie
        self.column_names['czesc_mowy'] = 'grammatical_part_of_speech'
        self.column_names['osoba'] = 'grammatical_person'
        self.column_names['czas'] = 'grammatical_tense'
        self.column_names['numer'] = 'grammatical_number'



    def define_czesci_mowy(self):
        self.czesc_mowy[0] = "rzeczownik"
        self.czesc_mowy[1] = "czasownik" # odmiana przez liczby, osoby, strony, czasy,
        self.czesc_mowy[2] = "przymiotnik" # odmiana przez przypadki, liczby, rodzaje
        self.czesc_mowy[3] = "liczebnik"
        self.czesc_mowy[4] = "zaimek"
        self.czesc_mowy[6] = "przysłówek"
        self.czesc_mowy[7] = "przysłówek"
        self.czesc_mowy[10] = "wykrzyknik" #ach, och, hej, oj, aj
        self.czesc_mowy[11] = "przyimek" # nad, wśród, ponad
        self.czesc_mowy[12] = "liczebnik"

    def define_czasy(self):
        self.czas[0] = "teraźniejszy"
        self.czas[1] = "przeszły"
        self.czas[2] = "przyszły"

    def define_rodzaje(self):
        self.rodzaj[0] = "męski"
        self.rodzaj[1] = "żeński"
        self.rodzaj[2] = "nijaki"

    def define_osoby(self):
        self.osoba[0] = "ja"
        self.osoba[1] = "ty"
        self.osoba[2] = "on"
        self.osoba[3] = "ona"
        self.osoba[4] = "ono"
        self.osoba[5] = "my"
        self.osoba[6] = "wy"
        self.osoba[7] = "oni"

    def define_przypadki(self):
        self.przypadek[0] = "mianownik"
        self.przypadek[1] = "dopełniacz"
        self.przypadek[2] = "celownik"
        self.przypadek[3] = "biernik"
        self.przypadek[4] = "narzędnik"
        self.przypadek[5] = "miejscownik"
        self.przypadek[6] = "wołacz"

    def define_liczby(self):
        self.liczba[0] = 'pojedyncza'
        self.liczba[1] = 'mnoga'


class LinguisticConverterEng:
    def __init__(self):
        self.part_of_speech = {} #rzecz, przym, itd.
        self.gender = {} # rodzaj
        self.case = {} # przypadki
        self.person = {}
        self.tense = {} # czas
        self.number = {} # l.poj, l.mnog

        self.define_part_of_speech()
        self.define_gender()
        self.define_case()
        self.define_person()
        self.define_tense()
        self.define_number()

    def get_number(self, word: Word):
        attr_in_raw_form = word.get_number()
        attr_converted = self.pl_number[attr_in_raw_form]
        return attr_converted


    def define_part_of_speech(self):
        self.part_of_speech[0] = "noun"
        self.part_of_speech[1] = "verb"
        self.part_of_speech[2] = "adjective"
        self.part_of_speech[3] = "numeral" # liczebnik
        self.part_of_speech[4] = "pronoun"  # zaimek
        self.part_of_speech[6] = "adverb"  # przysłówek

    def define_gender(self):
        self.gender[0] = "masculine"
        self.gender[1] = "feminine"
        self.gender[2] = "neuter"

    # grammatical_case
    def define_case(self):
        self.case[0] = "nominative" # mianownik
        self.case[1] = "genitive" # dopełniacz
        self.case[2] = "dative" # celownik
        self.case[3] = "accusative" # biernik
        self.case[4] = "instrumental" # narzędnik
        self.case[5] = "locative" # miejscownik
        self.case[6] = "vocative" # wołacz

    def define_person(self):
        self.person[0] = "I"
        self.person[1] = "You"
        self.person[2] = "He"
        self.person[3] = "She"
        self.person[4] = "It"
        self.person[5] = "We"
        self.person[6] = "You"
        self.person[7] = "They"

    def define_tense(self):
        self.tense[0] = "present"
        self.tense[1] = "past"
        self.tense[2] = "future"

    def define_number(self):
        self.number[0] = 'singuar'
        self.number[1] = 'plural'