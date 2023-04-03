import typer
import kontakty_orm as k

app = typer.Typer()


# add_contact
# list_contacts
# delete_contact


@app.command(name='add_contact')
def add_contact(first_name: str,
                last_name: str,
                age: int = typer.Argument(None, help='Wiek w latach'),
                email: str = None,
                phone: str = None):
    """
    Dodawanie rekordow do bazy.
    """
    e = k.connect()
    id = k.add_contact(e, first_name, last_name, age, email, phone)
    print('Dodano rekord id', id)


# @app.command()
# def delete_contact(id: int):
#     c = k.connect()
#     k.delete_id(id)
#     print(f'rekord id {id} usunięty jeżeli istniał.')


@app.command()
def query_contacts(first_name: str = None,
                   last_name: str = None,
                   age: int = None,
                   email: str = None,
                   phone: str = None):
    e = k.connect()
    lista_kontaktow = k.query_contacts(e, first_name, last_name, age, email, phone)
    print('Lista rekordów:')
    print('--------------\n')
    for c in lista_kontaktow:
        print(f'Imie: {c.first_name}, Nazwisko: {c.last_name}, email: {c.email}, Tel: {c.phone}')


if __name__ == '__main__':
    app()
