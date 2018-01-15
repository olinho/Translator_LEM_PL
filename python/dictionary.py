
class Word:
    def __init__(self, base_form: str):
        self.__base_form = base_form
        self.__attributes = {}

    def add_attribute(self, key, val):
        self.__attributes[key] = val

    def get_attributes(self):
        return self.__attributes

    def get_number(self):
        return self.__get_attribute('liczba')

    def __get_attribute(self, attr: str):
        return self.__attributes[attr]

    def get_base_form(self):
        return self.__base_form

    def get(self):
        dict = {self.__base_form: self.__attributes}
        return dict


class Dictionary:
    def __init__(self):
        self.dict = {}

    def add_word(self, word: Word):
        self.update(word.get())

    def update(self, newEl: {}):
        self.dict.update(newEl)

    def update_word(self, word: str, attribute: str, value: str):
        self.dict[word][attribute] = value

    def show(self):
        for attr, val in self.dict.items():
            print(str(attr) + ": " + str(val))



word = Word("бык")
word.add_attribute("rodzaj", "męski")
word.add_attribute("liczba", 0)
word.add_attribute("część mowy", "rzeczownik")

lem_dict = Dictionary()
lem_dict.add_word(word)
# lem_dict.show()
