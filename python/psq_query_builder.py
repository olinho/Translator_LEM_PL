

class QueryBuilder:
    def __init__(self):
        self.__where = ""
        self.__limit = "10"
        self.__order_by = ""
        self.__order = "ASC"
        self.__columns = "*"
        self.__columnsAsList = []
        self.__table = ""
        self.__query = QueryClass()


    def get_query(self):
        try:
            if self.__table == "":
                raise Exception("Table is not set")
            elif not self.__columnsAsList.__contains__(self.__order_by):
                raise Exception("Order by unknown column")
            else:
                self.__build_query()
                return self.__query.get_as_str()
        except Exception as e:
            print(e)

    def __build_query(self):
        self.__query.startQuery()\
            .appendColumnsClause(self.__columns)\
            .appendTableClause(self.__table)\
            .appendWhereClause(self.__where)\
            .appendOrderByClause(self.__order_by)\
            .appendOrderClause(self.__order)\
            .appendLimitClause(self.__limit)


    def setTable(self, table):
        self.__table = table
        return self

    def setAscOrderBy(self, order_by):
        self.__order = "ASC"
        return self.__setOrderBy(order_by)

    def setDescOrderBy(self, order_by):
        self.__order = "DESC"
        return self.__setOrderBy(order_by)

    def __setOrderBy(self, order_by):
        self.__order_by = order_by
        return self

    def setLimit(self, limit):
        self.__limit = limit
        return self

    def setWhere(self, whereClause):
        self.__where = whereClause
        return self

    def setColumns(self, cols: list):
        self.__columnsAsList = cols
        self.__columns = ", ".join(cols)
        return self

    def getColumnsAsString(self):
        return ", ".join(self.__columns)


class QueryClass:
    def __init__(self):
        self.__query = ""

    def get_as_str(self):
        return self.__query

    def __add(self, nextClause: str):
        self.__query += nextClause
        return self

    def appendLimitClause(self, clause):
        if clause != "":
            self.__add("LIMIT " + str(clause))
        return self

    def appendOrderClause(self, clause: str):
        if clause != "":
            self.__add(clause + " ")
        return self

    def appendOrderByClause(self, clause: str):
        if clause != "":
            self.__add("ORDER BY " + clause + " ")
        return self

    def appendWhereClause(self, clause: str):
        if clause != "":
            self.__add("WHERE " + clause + " ")
        return self

    def appendTableClause(self, clause: str):
        if clause != "":
            self.__add("FROM " + clause + " ")
        return self

    def appendColumnsClause(self, clause: str):
        if clause != "":
            self.__add(clause + " ")
        return self

    def startQuery(self):
        self.__add("SELECT ")
        return self

