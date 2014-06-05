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
        print "Handling motion: %s" % motion['_id']

        for vote_event in motion.get('vote_events'):
            # Short cut for 1:1 motion:vote_event cases
            vote_event_id = vote_event.get('id') or "VE-%s" % motion['_id']
            vote_event['_id'] = vote_event_id
            vote_event['id'] = vote_event_id
            vote_event['motion_id'] = motion['_id']

            seen_votes = set()
            for vote in vote_event.get('votes'):
                # Ensure we have at least a skeleton party
                # TODO add pre-defined attributes here
                if not vote.get('party') and not vote.get('party_id'):
                    raise Exception('Vote %s has no party or party_id' % vote['id'])
                if not vote.get('party'):
                    vote['party'] = { 'id': vote['party_id'] }
                if not vote.get('party_id'):
                    if not vote['party'].get('id'):
                        raise Exception('party %s has no id' % vote['party'])
                    vote['party_id'] = vote['party']['id']

                # Ensure we have at least a skeleton voter 
                if not vote.get('voter') and not vote.get('voter_id'):
                    raise Exception('Vote %s has no voter or voter_id' % vote['id'])
                if not vote.get('voter'):
                    vote['voter'] = { 'id': vote['voter_id'] }
                if not vote.get('voter_id'):
                    if not vote['voter'].get('id'):
                        raise Exception('voter %s has no id' % vote['voter'])
                    vote['voter_id'] = vote['voter']['id']

                vote['_id'] = vote.get('id') or "V-%s-%s" % (vote_event_id, vote.get('voter_id'))
                if vote['_id'] in seen_votes:
                  raise Exception("Duplicate vote %s " % vote['_id'])
                seen_votes.add(vote['_id'])
                vote['id'] = vote['_id']
                vote['weight'] = vote.get('weight') or 1
                vote['vote_event_id'] = vote_event_id
                vote['motion_id'] = motion['_id']

            votes.insert(vote_event.get('votes'))

        vote_events.insert(motion.get('vote_events'))

    motions.insert(data)

