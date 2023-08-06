from pymongo import MongoClient

client = MongoClient("localhost:27017",
                     username='admin',
                     password='w00d4th3s0u1',
                     authSource='admin')

db = client.get_database('fti_project')

answers = db.answers_2023.find()

s = set()
for answer in answers:
    for key in answer.keys():
        s.add(key)

print(s)