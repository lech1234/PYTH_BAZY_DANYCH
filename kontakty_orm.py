from pprint import pprint

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import faker
import faker as fk
import unidecode as ud

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    email = Column(String)
    phone = Column(String)

    def __repr__(self):
        return f"Contact(id={self.id}, name={self.first_name} {self.last_name}, age={self.age}, email={self.email}, phone={self.phone})"


def connect(baza='baza_orm.db') -> Engine:
    """
    :param baza: nazwa pliku sqlite
    :return: engine sqlalchemy
    """
    engine = create_engine(f"sqlite+pysqlite:///{baza}", echo=True, future=True)
    return engine


def create_all(engine: Engine):
    """
    Create tables.

    :param engine: db engine
    """
    Base.metadata.create_all(engine)


def drop_all(engine: Engine):
    Base.metadata.clear()


def add_contact(engine: Engine,
                first_name: str,
                last_name: str,
                age: int | None = None,
                email: str | None = None,
                phone: str | None = None) -> int:
    """
    Funkcja dodająca kontakty.


    :param engine: engine
    :param first_name:
    :param last_name:
    :param age:
    :param email:
    :param phone:
    :return: id dodanego rekordu
    """
    with Session(engine) as session:
        c = Contact(first_name=first_name,
                    last_name=last_name,
                    age=age,
                    email=email,
                    phone=phone)
        session.add(c)
        session.commit()
        return c.id


def query_contacts(engine: Engine,
                   first_name: str | None = None,
                   last_name: str | None = None,
                   age: int | None = None,
                   email: str | None = None,
                   phone: str | None = None) -> [Contact]:
    with Session(engine) as session:
        q = select(Contact)
        if first_name:
            q = q.where(Contact.first_name.like(first_name))
        if last_name:
            q = q.where(Contact.last_name.like(last_name))
        if age:
            q = q.where(Contact.age == age)
        if email:
            q = q.where(Contact.email.like(email))
        if phone:
            q = q.where(Contact.phone.like(phone))
        print(q)
        return [c for c in session.scalars(q)]


# def delete_id(engine: Engine, id):
#     with Session(engine) as session:
#         q = select(Contact).where(Contact.id == id)
#         session.delete(q)
#         session.commit()


def fill_data(engine: Engine, no_contacts=10):
    f = faker.Faker('PL-pl')
    for _ in range(no_contacts):
        f_n = f.first_name()
        l_n = f.last_name()
        age = f.random_int(18, 99)
        email = f'{ud.unidecode(f_n.lower())}.{ud.unidecode(l_n.lower())}@{f.domain_name()}'
        phone = f.phone_number()
        add_contact(engine, f_n, l_n, age, email, phone)


if __name__ == '__main__':
    e = connect()
    # drop_all(e)
    # create_all(e)
    # fill_data(e)
    # pprint(query_contacts(e, first_name='A%'))

