import sqlite3


class knightclient:

    connection = sqlite3.connect("knightstudio")
    cursor = connection.cursor()

    def update_data(self, key, value):
        pass

    def load_data(self, which):
        pass

    def insert_data(self, quer):
        pass
