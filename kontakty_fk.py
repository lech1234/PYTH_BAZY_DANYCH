import sqlite3
import faker


def connect(baza='baza_fk.db') -> sqlite3.Cursor:
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

    SQL_CREATE_TABLE_2 = '''CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        borrowed_from INTEGER NOT NULL,
        FOREIGN KEY (borrowed_from)
            REFERENCES contacts(contact_id)
            ON DELETE RESTRICT
        );'''
    c.execute(SQL_CREATE_TABLE_2)
    c.connection.commit()


# def drop_all(c: sqlite3.Cursor):
#     """
#     Drop all tables. Najwygodniej skasować plik.
#
#     :param c: db cursor
#     :return:
#     """


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
    return c.lastrowid


def add_book(c: sqlite3.Cursor,
             title: str,
             author: str,
             borrowed_from: int) -> int:
    """
    Funkcja dodająca książki.


    :param c: db cursor
    :param title:
    :param author:
    :param borrowed_from:
    :return: id dodanego rekordu
    """
    SQL_INSERT = '''INSERT INTO books (title, author, borrowed_from)
    VALUES
        (?, ?, ?);'''
    c.execute(SQL_INSERT, (title, author, borrowed_from))
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


def query_books(c: sqlite3.Cursor,
                title: str | None = None,
                author: str | None = None,
                borrowed_from: int | None = None) -> sqlite3.Cursor:
    if any((title, author, borrowed_from)):
        SQL_SELECT = 'SELECT * FROM books WHERE {};'
    else:
        SQL_SELECT = 'SELECT * FROM books {};'
    WHERE_TEMPLATE = '{} LIKE ?'
    WHERE = []
    if title:
        WHERE.append(WHERE_TEMPLATE.format('title'))
    if author:
        WHERE.append(WHERE_TEMPLATE.format('author'))
    if borrowed_from:
        WHERE.append(f'borrowed_from = ?')
    WHERE_STR = '\nand '.join(WHERE)
    SQL_DONE = SQL_SELECT.format(WHERE_STR)
    c.execute(SQL_DONE, [v for v in (title, author, borrowed_from) if v])
    return c


def query_books_joined(c: sqlite3.Cursor,
                       title: str | None = None,
                       author: str | None = None,
                       borrowed_from: int | None = None) -> sqlite3.Cursor:
    if any((title, author, borrowed_from)):
        SQL_SELECT = 'SELECT * FROM books l INNER JOIN contacts r ON r.contact_id = l.borrowed_from WHERE {};'
    else:
        SQL_SELECT = 'SELECT * FROM books l INNER JOIN contacts r ON r.contact_id = l.borrowed_from {};'
    WHERE_TEMPLATE = '{} LIKE ?'
    WHERE = []
    if title:
        WHERE.append(WHERE_TEMPLATE.format('l.title'))
    if author:
        WHERE.append(WHERE_TEMPLATE.format('l.author'))
    if borrowed_from:
        WHERE.append(f'l.borrowed_from = ?')
    WHERE_STR = '\nand '.join(WHERE)
    SQL_DONE = SQL_SELECT.format(WHERE_STR)
    c.execute(SQL_DONE, [v for v in (title, author, borrowed_from) if v])
    return c


def fill_data(c: sqlite3.Cursor, no_contacts=10, no_books=5):
    f = faker.Faker('PL:pl')
    for _ in range(no_contacts):
        id = add_contact(c, f.first_name(), f.last_name(), f.random_int(18, 99), f.email(), f.phone_number())
        for _ in range(no_books):
            add_book(c, f.sentence(), f.name(), id)
    c.connection.commit()


if __name__ == '__main__':
    c = connect()
    # drop_all(c)
    # create_all(c)
    # fill_data(c)
    print('Zawartość bazy:')
    # for r in query_contacts(c):
    #     print(r)
    # for r in query_books(c):
    #     print(r)
#     c.execute('''SELECT l.*, r.*
# FROM
#     books l
# INNER JOIN contacts r ON
#     r.contact_id = l.borrowed_from;''')
    c = query_books_joined(c, author='S%')
    for _, tytul, autor, _, _, imie, nazwisko, wiek, email, tel in c:
        print(tytul, autor, imie)
    