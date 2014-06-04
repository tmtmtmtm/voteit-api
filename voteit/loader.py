from pprint import pprint

from voteit.core import motions, vote_events
from voteit.core import vote_counts, votes
from voteit.core import persons, parties

def reload_people(data):
    for person in data:
        print "PER Loading: %s" % person.get('name')
        person['@type'] = 'Person'
        persons.update({'id': person.get('id')}, person, upsert=True)


def reload_parties(data):
    for party in data:
        print "PTY Loading: %s" % party.get('name')
        party['@type'] = 'Party'
        parties.update({'id': party.get('id')}, party, upsert=True)


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


def reload_vote(vote, vote_event, motion, data):
    vote['weight'] = 1
    vote['vote_event_id'] = vote_event.get('id')
    vote['motion_id'] = motion.get('id')
    votes.update({'vote_event_id': vote_event.get('id'), 'voter_id': vote.get('voter_id')}, vote, upsert=True)
