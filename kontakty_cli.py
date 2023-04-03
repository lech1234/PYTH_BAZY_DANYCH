import typer
import kontakty as k

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
    c = k.connect()
    id = k.add_contact(c, first_name, last_name, age, email, phone)
    print('Dodano rekord id', id)


@app.command()
def delete_contact(id: int):
    c = k.connect()
    k.delete_id(id)
    print(f'rekord id {id} usunięty jeżeli istniał.')


@app.command()
def query_contacts(first_name: str = None,
                   last_name: str = None,
                   age: int = None,
                   email: str = None,
                   phone: str = None):
    c = k.connect()
    k.query_contacts(c, first_name, last_name, age, email, phone)
    print('Lista rekordów:')
    print('--------------\n')
    for id, f_n, l_n, _, email, phone in c:
        print(f'Imie: {f_n}, Nazwisko: {l_n}, email: {email}, Tel: {phone}')


if __name__ == '__main__':
    app()
