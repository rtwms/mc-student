from abc import ABC, abstractmethod


class Datalayer(ABC):
    def __init__(self, dbtype='sqlite3', dbname='database.db'):
        self.dbtype = dbtype
        self.dbname = dbname

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def insert(self, statement):
        pass

    @abstractmethod
    def update(self, statement):
        pass

    @abstractmethod
    def delete(self, statement):
        pass

    @abstractmethod
    def search(self, statement):
        pass