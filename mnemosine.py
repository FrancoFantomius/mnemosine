import sqlite3


class database():
    def __init__(self, path):
        self.path = path + "index.db"
        conn_index = sqlite3.connect(self.path)
        self.curs = conn_index.cursor()
    #read the index to find the right database to put the data in
    def guide(self, data):
        for n in range(len(data)):
            
