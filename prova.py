"""import sqlite3 
conn = sqlite3.connect('index.db') 
c = conn.cursor()

#c.execute('''CREATE TABLE indx(id INTEGER, par TEXT, specific NUMERIC, path TEXT)''')

#c.execute(''' INSERT INTO indx (id, par, specific, path) VALUES(1, 'a', 1, 'C:/Users/franc/OneDrive/Programmazione/2021/Mnemosine/a.db') ''')
#c.execute(''' INSERT INTO indx (id, par, specific, path) VALUES(2, "b", 0, "indx1") ''')
#conn.commit()

c.execute('''SELECT * FROM indx''') 
data = [] 
for row in c.fetchall(): 
    data.append(row)
print(data)"""

data = "ciao"

for a in range(len(data)):
    print(data[a])