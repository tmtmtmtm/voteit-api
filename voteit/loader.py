from pprint import pprint

from voteit.core import motions, vote_events
from voteit.core import vote_counts, votes
from voteit.core import persons, parties

def reload_people(data):
    for person in data:
        print "PER Loading: %s" % person.get('name')
        person['@type'] = 'Person'
        persons.update({'id': person.get('id')}, person, upsert=True)

def bulk_load_people(data):
    for doc in data:
        doc['_id'] = doc.get('id')
    persons.insert(data)


def reload_parties(data):
    for party in data:
        print "PTY Loading: %s" % party.get('name')
        party['@type'] = 'Party'
        parties.update({'id': party.get('id')}, party, upsert=True)

def bulk_load_parties(data):
    for doc in data:
        doc['_id'] = doc.get('id')
    parties.insert(data)


def reload_motions(data):
    for motion in data:
        motion_id = motion.get('id') 
        print "Motion: %s" % motion_id

        motions.update({'id': motion_id}, motion, upsert=True)

        for vote_event in motion.get('vote_events'):
            vote_event_id = vote_event.get('id') or "VE-%s" % motion_id
            vote_event['id'] = vote_event_id
            vote_event['motion_id'] = motion_id
            vote_events.update({'id': vote_event_id}, vote_event, upsert=True)

            for count in vote_event.get('counts'):
                count['vote_event_id'] = vote_event_id
                vote_counts.update({'vote_event_id': vote_event_id, 'option': count.get('option')}, count, upsert=True)

            for vote in vote_event.get('votes'):
                reload_vote(vote, vote_event, motion, data)

def bulk_load_motions(data):
    for motion in data:
        motion['_id'] = motion.get('id')
        print "Inserting motion: %s" % motion['_id']

        for vote_event in motion.get('vote_events'):
            # Short cut for 1:1 motion:vote_event cases
            vote_event_id = vote_event.get('id') or "VE-%s" % motion['_id']
            vote_event['_id'] = vote_event_id
            vote_event['id'] = vote_event_id
            vote_event['motion_id'] = motion['_id']

            # Do we need these at all?
            for vote_count in vote_event.get('counts'):
                vote_count['_id'] = vote_count.get('id') or "VC-%s-%s" % (vote_event_id, vote_count.get('option'))
                vote_count['id'] = vote_count['_id']
                vote_count['vote_event_id'] = vote_event_id
            vote_counts.insert(vote_event.get('counts'))

            for vote in vote_event.get('votes'):
                vote['_id'] = vote.get('id') or "V-%s-%s" % (vote_event_id, vote.get('voter_id'))
                vote['id'] = vote['_id']
                vote['weight'] = vote.get('weight') or 1
                vote['vote_event_id'] = vote_event_id
                vote['motion_id'] = motion['_id']
            votes.insert(vote_event.get('votes'))

        vote_events.insert(motion.get('vote_events'))

    motions.insert(data)


def reload_vote(vote, vote_event, motion, data):
    vote['weight'] = 1
    vote['vote_event_id'] = vote_event.get('id')
    vote['motion_id'] = motion.get('id')
    votes.update({'vote_event_id': vote_event.get('id'), 'voter_id': vote.get('voter_id')}, vote, upsert=True)
