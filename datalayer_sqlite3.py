import sqlite3 as sql3
from datalayer_abstract import Datalayer


class DatalayerSqlite3(Datalayer):
    def __init__(self, dbname='database.db'):
        super().__init__()
        print('init with %s' % dbname)
        self.dbname = dbname
        self.dbc = None  # sql3.connect(self.dbname)
        self.cursor = None  # self.dbc.cursor()

    def connect(self):
        self.dbc = sql3.connect(self.dbname)
        self.cursor = self.dbc.cursor()
        return self.dbc, self.cursor

    def update(self, statement):
        dbc, cursor = self.connect()

        try:
            result = cursor.execute(statement)
        except Exception as e:
            print(e)

        dbc.commit()
        dbc.close()
        print('done saving %s' % (result))

        return result

    def insert(self, statement):
        dbc, cursor = self.connect()

        try:
            result = cursor.execute(statement)
        except Exception as e:
            result = None
            print(e)

        dbc.commit()
        dbc.close()

        return result

    def delete(self, statement):
        dbc, cursor = self.connect()

        try:
            result = cursor.execute(statement)
        except Exception as e:
            result = None
            print(e)

        dbc.commit()
        dbc.close()

        return result

    def search(self, statement):
        dbc, cursor = self.connect()
        data = []
        try:
            result = cursor.execute(statement)
            for row_idx, row in enumerate(result):
                data.append((row_idx, row))
        except Exception as e:
            print(e)

        dbc.close()

        return data
