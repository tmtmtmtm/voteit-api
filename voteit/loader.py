from pprint import pprint

from voteit.core import motions, vote_events, votes
from voteit.core import persons, parties

def bulk_load_people(data):
    for doc in data:
        doc['_id'] = doc.get('id')
    persons.insert(data)


def bulk_load_parties(data):
    for doc in data:
        doc['_id'] = doc.get('id')
    parties.insert(data)


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

            for vote in vote_event.get('votes'):
                vote['_id'] = vote.get('id') or "V-%s-%s" % (vote_event_id, vote.get('voter_id'))
                vote['id'] = vote['_id']
                vote['weight'] = vote.get('weight') or 1
                vote['vote_event_id'] = vote_event_id
                vote['motion_id'] = motion['_id']
            votes.insert(vote_event.get('votes'))

        vote_events.insert(motion.get('vote_events'))

    motions.insert(data)

