from pymongo import MongoClient

import wikirate4py

client = MongoClient("localhost:27017",
                     username='admin',
                     password='w00d4th3s0u1',
                     authSource='admin')

db = client.get_database("msa_assessed")

api = wikirate4py.API('NzSK5muu3o7oSwDa2PpUVQtt')

statements = db.uk_assessed_0523.find({"verified": True})

for statement in statements:
    print('Statement ID: {0}'.format(statement['_id']))
    unverified_answer_ids: [] = statement['unverified_answers_ids']
    unverified_answers: [] = statement['unverified_answers']
    verified_answer_ids: [] = statement['verified_answers_ids']
    verified_answers: [] = statement['verified_answers']

    for id in unverified_answer_ids.copy():
        print(id)
        response = api.verify_answer(id)
        checked_by = response.json()
        name = checked_by['name'].split('+')
        unverified_answer_ids.remove(id)
        verified_answer_ids.append(id)
        verified_answers.append('{0}+{1}'.format(name[0], name[1]))
        unverified_answers.remove('{0}+{1}'.format(name[0], name[1]))

    db.uk_assessed_0523.update_one({'_id': statement['_id']}, {
        '$set': {'unverified_answers_ids': unverified_answer_ids,
                 'verified_answers_ids': verified_answer_ids,
                 'verified_answers': verified_answers,
                 'unverified_answers': unverified_answers}})

    print(statement['url'])

