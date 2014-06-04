import json

from flask.ext.script import Manager

from voteit.core import db
from voteit.web import app
from voteit.loader import reload_motions, bulk_load_motions
from voteit.loader import reload_parties, bulk_load_parties
from voteit.loader import reload_people, bulk_load_people


manager = Manager(app)

@manager.command
def loadfile(file_name):
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        reload_parties(data.get('parties', {}).values())
        reload_people(data.get('people', {}).values())
        reload_motions(data.get('motions', []))

@manager.command
def reloadpeople(file_name):
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        reload_people(data)

@manager.command
def bulkloadpeople(file_name):
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        bulk_load_people(data)


@manager.command
def reloadparties(file_name):
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        reload_parties(data)

@manager.command
def bulkloadparties(file_name):
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        bulk_load_parties(data)


@manager.command
def reloadmotions(file_name):
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        reload_motions(data)

@manager.command
def bulkloadmotions(file_name):
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        bulk_load_motions(data)

@manager.command
def reset():
    for coll in db.collection_names():
        if coll in ['system.indexes', 'system.users']:
            continue
        print coll
        db.drop_collection(coll)

@manager.command
def deletemotions():
    db.drop_collection('votes')
    db.drop_collection('vote_counts')
    db.drop_collection('vote_events')
    db.drop_collection('motions')

@manager.command
def deletepeople():
    db.drop_collection('persons')

@manager.command
def deleteparties():
    db.drop_collection('parties')

def run():
    manager.run()

if __name__ == "__main__":
    run()
