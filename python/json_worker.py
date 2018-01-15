import json

class LemkoWordsJSON:
    def __init__(self):
        self.dict = {}
        self.load_data_from_file()

    def load_data_from_file(self):
        with open("data/lemko_words.json", "r", encoding="utf8") as file:
            self.dict = json.load(file)

    def update_dict(self, el: {}):
        node_key = self.get_node_key(el)
        node_value = self.get_node_value(el)
        self.dict[node_key] = node_value


    def get_node_value(self, el: {}) -> {}:
        return list(el.values())[0]

    def get_node_key(self, el: {}) -> {}:
        return list(el.keys())[0]

    def save_file(self):
        with open('data/lemko_words.json', 'wb') as file:
            file.write(
                json.dumps(self.dict, indent=2, sort_keys=False, ensure_ascii=False).encode('utf8'))

    def show_dict(self):
        print(self.dict)

    def get_dict(self):
        return self.dict
