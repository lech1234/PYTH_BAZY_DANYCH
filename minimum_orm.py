from pprint import pprint

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine

Base = declarative_base()


class Dog(Base):
    __tablename__ = "dogs"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    breed = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"Dog(id={self.id}, name={self.name}, breed={self.breed}, age={self.age}"

if __name__ == '__main__':
    engine = create_engine("sqlite://", echo=True, future=True)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        u1 = Dog(name='Azor',
                  age=3,
                  breed='maliniak')
        u2 = Dog(name='Sara',
                  age=13,
                  breed='owczarek')
        u3 = Dog(name='Alina')
        session.add_all([u1, u2, u3])
        print('New records:')
        pprint(list(session.new))
        print()
        session.commit()
        stmt = select(Dog).where(Dog.name.like('A%'))
        for c in session.scalars(stmt):
            print(c)

        stmt = select(Dog).where(Dog.name == 'Azor')
        for c in session.scalars(stmt):
            print(c)

        c = session.scalars(select(Dog).where(Dog.name == 'Alina')).first()
        print(c)
        c.age = 4
        print('Dirty:')
        print('-----:')
        pprint(list(session.dirty))
        print()
        session.commit()
        print('Dirty:')
        print('-----:')
        pprint(list(session.dirty))
        print()
