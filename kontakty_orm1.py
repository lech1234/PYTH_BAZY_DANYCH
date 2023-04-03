from pprint import pprint

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

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

if __name__ == '__main__':
    engine = create_engine("sqlite://", echo=True, future=True)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        u1 = Contact(first_name='Ala',
                  last_name='Kowalik',
                  age=33,
                  email='ala@kowalik.com',
                  phone='333444555')
        u2 = Contact(first_name='Alek',
                  last_name='Kowalik')
        u3 = Contact(first_name='Paweł',
                  last_name='Nowak',
                  age=35)
        session.add_all([u1, u2, u3])
        print('New records:')
        pprint(list(session.new))
        print()
        session.commit()
        stmt = select(Contact).where(Contact.last_name.like('K%'))
        for c in session.scalars(stmt):
            print(c)

        stmt = select(Contact).where(Contact.last_name == 'Kowalik')
        for c in session.scalars(stmt):
            print(c)

        c = session.scalars(select(Contact).where(Contact.last_name == 'Kowalik')).first()
        print(c)
        c.age = 44
        print('Dirty:')
        print('-----:')
        pprint(list(session.dirty))
        print()
        session.commit()
        print('Dirty:')
        print('-----:')
        pprint(list(session.dirty))
        print()
