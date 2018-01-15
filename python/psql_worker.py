
import psycopg2
import utils

from psq_query_builder import QueryBuilder

connection = None
database = "de3ouqf0021868_98"
user = "postgres"
password = "postgres"

class PsqlWorker:
    def __init__(self):
        self.__connection = None
        self.__hostname = "localhost"
        self.__database = "de3ouqf0021868_98"
        self.__user = "postgres"
        self.__password = "postgres"
        self.__tables = []
        self.__connect()
        self.__query_tables()


    def get_word_details(self, word: str):
        cols = ["base_form", "polish_translation", "grammatical_gender", "grammatical_part_of_speech"]
        cols_as_str = ",".join(cols)
        query = "SELECT " + cols_as_str + " " \
                "FROM terms " \
                "WHERE base_form = %s " \
                "LIMIT 1"
        resp = self.do_query(query, (word,), cols)
        return resp

    def show_word_details(self, word: str):
        self.show_zip(self.get_word_details(word))

    def show_zip(self, zipped):
        for key, val in zipped:
            print(key, ":", val)

    def get_part_of_speech(self, word: str):
        query = "SELECT grammatical_part_of_speech FROM terms WHERE base_form = %s LIMIT 1"
        resp = self.do_query(query, (word,))
        return utils.unnest_list(resp)

    def get_conjugation(self, word: str):
        cols = ["word", "grammatical_person", "grammatical_tense"]
        cols_as_str = ",".join(cols)
        query = "SELECT " + cols_as_str + " " \
                "FROM terms as T " \
                "JOIN term_word_associations as ASS " \
                "ON (T.id  = ASS.term_id) " \
                "WHERE base_form = %s " \
                " AND T.id in (SELECT id FROM terms WHERE base_form = T.base_form limit 1) " \
                " AND word != '' " \
                "ORDER BY 1, 2; "
        resp = self.do_query(query, (word,), cols)
        return resp

    def get_noun_declination(self, word: str):
        cols = ["word", "grammatical_number", "grammatical_case"]
        cols_as_str = ",".join(cols)
        query = "SELECT " + cols_as_str + " " \
                "FROM terms as T " \
                "JOIN term_word_associations as ASS " \
                "ON (T.id  = ASS.term_id) " \
                "WHERE T.base_form = %s " \
                " AND T.id in (select id from terms where base_form = T.base_form limit 1) " \
                " AND word != '' " \
                "ORDER BY 2, 3"
        resp = self.do_query(query, (word,), cols)
        return resp

    def get_adjective_declination(self, word: str):
        cols = ["word", "grammatical_number", "grammatical_case", "grammatical_comparison", "grammatical_gender"]
        cols_as_str = ",".join(cols)
        query = "SELECT " + cols_as_str + " " \
                "FROM term_word_associations " \
                "WHERE term_id in (select id from terms where base_form = %s limit 1) " \
                " AND word != '' " \
                "ORDER BY 2, 4, 5, 3"
        resp = self.do_query(query, (word,), cols)
        return resp

    def convert_response_to_list(self, resp):
        if len(resp) == 1:
            return list(resp[0])
        else:
            return [list(resp[i]) for i,_ in enumerate(resp)]

    def get_columns_in_table(self, table: str):
        query_str = "SELECT column_name from information_schema.columns where table_name = '" + table + "';"
        result = self.do_query(query_str)
        result_as_list = [self.parse_value(el) for el in result]
        return result_as_list

    def __query_tables(self):
        query_str = "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
        self.cur.execute(query_str)
        result = self.cur.fetchall()
        self.__tables = [list(t_name)[0] for t_name in result]

    def get_tables(self):
        return self.__tables

    def get_base_form_for_word(self, word: str):
        query = "SELECT CASE " \
                "WHEN EXISTS " \
                "(SELECT 1 from term_word_associations where word = %s) " \
                " THEN (SELECT base_form FROM terms WHERE id = " \
                    "(SELECT term_id FROM term_word_associations " \
                    " WHERE word = %s " \
                    " LIMIT 1)" \
                ") ELSE " \
                "(SELECT base_form from terms WHERE base_form = %s limit 1) " \
                " END;"
        self.cur.execute(query, (word,word,word))
        queryResult = self.cur.fetchone()
        base_form = self.parse_value(queryResult)
        return base_form

    def get_sentences_with_word(self, word: str):
        resultList = []
        query = "SELECT context1_body, context2_body, context3_body " \
                " FROM terms " \
                " WHERE base_form = %s "
        self.cur.execute(query, (word,))
        for queryResult in self.cur.fetchall():
            parsed_result = self.parse_value(queryResult)
            formatted_result = utils.format_text(str(parsed_result))
            resultList.append(formatted_result)
        return resultList

    def get_sentence_with_word(self, word: str):
        resultList = []
        query = "SELECT (CASE " \
                " WHEN context1_body != '' then context1_body " \
                " WHEN context2_body != '' then context2_body " \
                " WHEN context3_body != '' then context3_body " \
                " ELSE '' END) as context " \
                " FROM terms " \
                " WHERE base_form = %s " \
                " LIMIT 1"
        self.cur.execute(query, (word,))
        for queryResult in self.cur.fetchall():
            base_form = self.parse_value(queryResult)
            resultList.append(base_form)
        return resultList[0]

    def get_new_words(self, old_words: [], part_of_speech = -1, limit = 10, order = "asc"):
        whereClause = " editing_state = 2 "
        if len(old_words) > 0:
            whereClause += " AND LOWER(base_form) NOT IN %(old_words)s "
        if part_of_speech != -1:
            whereClause += " AND grammatical_part_of_speech = " + str(part_of_speech)
        resultList = []
        self.cur.execute("SELECT distinct(base_form) FROM terms WHERE " +
                         whereClause +
                         " ORDER BY base_form " + order +
                         " LIMIT " + str(limit), {'old_words': tuple(old_words)})
        for queryResult in self.cur.fetchall():
            base_form = self.parse_value(queryResult)
            resultList.append(base_form)
        return resultList

    def get_nouns_from_terms_table(self, limit=100, order="asc"):
        return self.get_words_from_the_part_of_speech(part_of_speech=0, limit=limit, order=order)

    def get_verbs_from_terms_table(self, limit=100, order="asc"):
        return self.get_words_from_the_part_of_speech(part_of_speech=1, limit=limit, order=order)

    def get_adjectives_from_terms_table(self, limit=100, order="asc"):
        return self.get_words_from_the_part_of_speech(part_of_speech=2, limit=limit, order=order)

    def get_words_from_the_part_of_speech(self, part_of_speech: int, limit=100, order="asc"):
        whereClause = "grammatical_part_of_speech = " + str(part_of_speech)\
                      + " AND editing_state = 2"
        resultList = []
        self.cur.execute("SELECT distinct(base_form) FROM terms "
                         " WHERE " + whereClause +
                         " ORDER BY base_form " + order +
                         " LIMIT " + str(limit))
        for queryResult in self.cur.fetchall():
            base_form = self.parse_value(queryResult)
            resultList.append(base_form)
        return resultList


    def do_query_where(self, whereClause):
        self.cur.execute("SELECT base_form from terms WHERE " +
                    whereClause + " limit 100")
        return self.cur.fetchall()

    def do_query(self, query: str, values= (), cols=[]):
        if len(values) == 0:
            self.cur.execute(query)
        else:
            self.cur.execute(query, values)
        resp = []
        i=0
        if len(cols) > 0:
            while True:
                row = self.cur.fetchone()
                if row == None:
                    break
                resp.append(dict(zip(cols, list(row))))
                i += 1
        else:
            while True:
                row = self.cur.fetchone()
                if row == None:
                    break
                resp.append(list(row))
                i += 1
        return resp



    def __connect(self):
        try:
            self.__connection = psycopg2.connect(host=self.__hostname,database=self.__database,user=self.__user,password=self.__password)
            self.cur = self.__connection.cursor()
        except psycopg2.DatabaseError as e:
            print('Error %s' % e)
            exit(1)

    def close(self):
        if self.__connection:
            self.__connection.close()

    def parse_value(self, el):
        return list(el)[0]

    def example_of_query_builder(self):
        queryBuilder = QueryBuilder()
        queryBuilder.setColumns(['base_form', 'polish_translation']) \
            .setTable("terms") \
            .setWhere("base_form like 'аба%' AND polish_translation != ''") \
            .setLimit(50) \
            .setAscOrderBy('base_form')
        query = queryBuilder.get_query()
        print(self.do_query(query))

