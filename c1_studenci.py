import sqlite3

# dbapi 2.0
conn = sqlite3.connect(':memory:')
# 1. Stworzyć tabelę 'contacts' zawierającą kolumny:
# - first_name - tekst - obowiązkowy
# - last_name - tekst - obowiązkowy
# - age - int
# - email - tekst
# - phone - test

SQL_CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS contacts (
    contact_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER,
    email TEXT,
    phone TEXT
    );
'''
SQL_DROP_TABLE = '''DROP TABLE IF EXISTS contacts;'''
c = conn.cursor()
c.execute(SQL_CREATE_TABLE)

c.execute('select name, sql from sqlite_master')
print('Schema bazy:')
for name, schema in c:
    print(name)
    print(schema)
c.execute(SQL_DROP_TABLE)
print('Schema bazy:')
c.execute('select name, sql from sqlite_master')
for name, schema in c:
    print(name)
    print(schema)
c.execute(SQL_CREATE_TABLE)

c.execute('select name, sql from sqlite_master')
print('Schema bazy:')
for name, schema in c:
    print(name)
    print(schema)

# 2. Dodać rekord do bazy:
#    Jan Kowalski
imie = 'Jan'
nazwisko = 'Kowalski'

SQL_INSERT = '''INSERT INTO contacts (first_name, last_name, age)
VALUES
    (?, ?, ?);'''

c.execute(SQL_INSERT, ('Jan', 'Kowalski', None))
print('Last row id: ', c.lastrowid)


print('Zawartość bazy:')
for id, first_name, last_name, age, email, phone in c.execute('select * from contacts'):
    print(id, first_name, last_name)
