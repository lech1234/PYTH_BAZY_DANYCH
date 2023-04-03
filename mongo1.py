from pprint import pprint
import faker
import pymongo.database
import bson.objectid


def connect() -> pymongo.database.Database:
    client = pymongo.MongoClient("mongodb+srv://user:passwd@cluster0.twlm0h0.mongodb.net/?retryWrites=true&w=majority")
    db: pymongo.database.Database = client.test
    return db


def fill_data(db: pymongo.database.Database, count=100):
    f = faker.Faker('PL:pl')
    d_list = [{'first_name': f.first_name(),
               'last_name': f.last_name(),
               'age': f.random_int(18, 99),
               'email': f.email(),
               'phone': f.phone_number()}
              for _ in range(count)]
    ludzie : pymongo.database.Collection = db.ludzie
    ludzie.insert_many(d_list)

def clear_all(db: pymongo.database.Database):
    ludzie: pymongo.database.Collection = db.ludzie
    ludzie.drop()

if __name__ == '__main__':
    db = connect()
    clear_all(db)
    fill_data(db)
    ludzie: pymongo.database.Collection = db.ludzie

    for x in ludzie.find({}):
        pprint(x)

# ludzie = db.ludzie
# ludzie.insert_one({'imie': 'Marek',
#                    'nazwisko': 'Kowalski'})
# for x in ludzie.find({'imie': 'Marek'}):
#     print(x)
# my_id = bson.objectid.ObjectId('63d5704f17701f916724f104')
# for x in ludzie.find({'_id': my_id}):
#     print(x)
