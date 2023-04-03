import sqlite3

import faker
import faker as fk
import unidecode as ud


def connect(baza='baza.db') -> sqlite3.Cursor:
    conn = sqlite3.connect(baza)
    return conn.cursor()


def create_all(c: sqlite3.Cursor):
    """
    Create tables.

    :param c: db cursor
    """
    SQL_CREATE_TABLE_1 = '''CREATE TABLE IF NOT EXISTS contacts (
        contact_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER,
        email TEXT,
        phone TEXT
        );'''
    c.execute(SQL_CREATE_TABLE_1)


def drop_all(c: sqlite3.Cursor):
    """
    Drop all tables.

    :param c: db cursor
    :return:
    """
    SQL_DROP_TABLE = '''DROP TABLE IF EXISTS contacts;'''
    c.execute(SQL_DROP_TABLE)


def add_contact(c: sqlite3.Cursor,
                first_name: str,
                last_name: str,
                age: int | None = None,
                email: str | None = None,
                phone: str | None = None) -> int:
    """
    Funkcja dodająca kontakty.


    :param c: db cursor
    :param first_name:
    :param last_name:
    :param age:
    :param email:
    :param phone:
    :return: id dodanego rekordu
    """
    SQL_INSERT = '''INSERT INTO contacts (first_name, last_name, age, email, phone)
    VALUES
        (?, ?, ?, ?, ?);'''
    c.execute(SQL_INSERT, (first_name, last_name, age, email, phone))
    c.connection.commit()
    return c.lastrowid


def query_contacts(c: sqlite3.Cursor,
                   first_name: str | None = None,
                   last_name: str | None = None,
                   age: int | None = None,
                   email: str | None = None,
                   phone: str | None = None) -> sqlite3.Cursor:
    if any((first_name, last_name, age, email, phone)):
        SQL_SELECT = '''SELECT * FROM contacts WHERE {};'''
    else:
        SQL_SELECT = '''SELECT * FROM contacts {};'''

    WHERE_TEMPLATE = '{} LIKE ?'
    WHERE = []
    if first_name:
        WHERE.append(WHERE_TEMPLATE.format('first_name'))
    if last_name:
        WHERE.append(WHERE_TEMPLATE.format('last_name'))
    if age:
        WHERE.append(f'age = ?')
    if email:
        WHERE.append(WHERE_TEMPLATE.format('email'))
    if phone:
        WHERE.append(WHERE_TEMPLATE.format('email'))
    WHERE_STR = '\nand '.join(WHERE)
    SQL_DONE = SQL_SELECT.format(WHERE_STR)
    print(SQL_DONE)
    c.execute(SQL_DONE, [v for v in (first_name, last_name, age, email, phone) if v])
    return c

def delete_id(c: sqlite3.Cursor, id):
    c.execute('DELETE FROM contacts WHERE contact_id = ?', (id,))
    c.connection.commit()


def fill_data(c: sqlite3.Cursor, no_contacts=10):
    f = faker.Faker('PL-pl')
    for _ in range(no_contacts):
        f_n = f.first_name()
        l_n = f.last_name()
        age = f.random_int(18, 99)
        email = f'{ud.unidecode(f_n.lower())}.{ud.unidecode(l_n.lower())}@{f.domain_name()}'
        phone = f.phone_number()
        add_contact(c, f_n, l_n, age, email, phone)


if __name__ == '__main__':
    c = connect()
    # drop_all(c)
    # create_all(c)
    fill_data(c)
    print('Zawartość bazy:')
    for r in query_contacts(c):
        print(r)
    print('Kasujemy')
    c.execute('DELETE FROM contacts WHERE contact_id=?', (58,))
    c.connection.commit()