from pprint import pprint

from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Dog(Base):
    __tablename__ = 'dogs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    breed = Column(String)

    def __repr__(self):
        return f'Dog(id={self.id}, name={self.name}, age={self.age}, breed={self.breed})'

    # def __str__(self):
    #     return 'alamakota str'

if __name__ == '__main__':
    engine = create_engine('sqlite+pysqlite:///db1.db', echo=True)
    Base.metadata.create_all(engine)
    # engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/mydatabase")
    # engine = create_engine("dialekt+biblioteka://user:haslo@host:port/baza")

    with Session(engine) as session:
        d1 = Dog(name='Azorek')
        d2 = Dog(name='Burek', age=13, breed='kundelek')
        d3 = Dog(name='Aza', age=3, breed='maliniak')
        d4 = Dog(name='Reks', breed='maliniak')
        lista = [d1, d2, d3, d4]
        pprint(lista)
        session.add_all(lista)
        pprint(lista)
        print(session.new)
        session.commit()
        pprint(lista)
        # uwaga - to jest przygotowane query - jeszcze nie poszło żadne zapytanie
        q1 = select(Dog)
        for d in session.scalars(q1):
            print(d)

        q1 = select(Dog).where(Dog.name.like('A%'))
        for d in session.scalars(q1):
            print(d)

        q1 = select(Dog).where(Dog.name == 'Azorek')
        for d in session.scalars(q1):
            print(d)
            d.age = 10
            print(session.dirty)
            session.commit()
            print(session.dirty)
        q1 = select(Dog).where(Dog.name == 'Azorek')
        for d in session.scalars(q1):
            print(d)
