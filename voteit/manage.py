import json

from flask.ext.script import Manager

from voteit.core import db, issues
from voteit.web import app
from voteit.loader import load_motions
from voteit.loader import load_parties, load_people


manager = Manager(app)


@manager.command
def loadfile(file_name):
    """ Load motions from a JSON file. """
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        load_parties(data.get('parties', {}).values())
        load_people(data.get('people', {}).values())
        load_motions(data.get('motions', []))

@manager.command
def loadpeople(file_name):
    """ Load people from a JSON file. """
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        load_people(data)

@manager.command
def loadparties(file_name):
    """ Load parties from a JSON file. """
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        load_parties(data)

@manager.command
def loadmotions(file_name):
    """ Load motions from a JSON file. """
    with open(file_name, 'rb') as fh:
        data = json.load(fh)
        load_motions(data)

@manager.command
def reset():
    for coll in db.collection_names():
        if coll in ['issues', 'system.indexes', 'system.users']:
            continue
        print coll
        db.drop_collection(coll)

@manager.command
def deleteissues():
    db.drop_collection(issues)

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


# todo: guarantee that motions exist...
@manager.command
def addtestissue():
    db.issues.insert({
        'title': 'Finnish Misogynist Union Stance',
        'phrase': 'making homophobia, xenophobia and supressed anger an art form',
        'motions': [{
            'motion_id': 'motion-62-2012-1',
            'weights': {'yes': 23}
        }, {
            'motion_id': 'motion-62-2012-2',
            'weights': {'yes': -23}
        }]
    })



def run():
    manager.run()

if __name__ == "__main__":
    run()
