from collections import defaultdict

from bson.code import Code
from bson.objectid import ObjectId

from voteit.core import votes, issues

REDUCE = Code("""
function(obj, prev) {
    if (!prev.votes.hasOwnProperty(obj.option)) {
        prev.votes[obj.option] = 0;
    }
    prev.votes[obj.option] += obj.weight;
    prev.num_votes += obj.weight;
};
""")


def get_options():
    options = votes.find({}).distinct('option')
    return options

def generate_aggregate(blocs=[], motion_ids=[], filters={}):
    keys = set(blocs)

    spec = dict(filters)
    if len(motion_ids):
      spec['motion_id'] = {'$in': motion_ids}
      keys.add('motion_id')

    options = get_options()

    data = {}
    for cell in votes.group(keys, spec, {"votes": {}, 'num_votes': 0}, REDUCE):

        key = repr([cell.get(k) for k in set(keys)])
        if not key in data:
            data[key] = {
                'counts': defaultdict(int),
                'bloc': {},
                'stats': {
                    'num_motions': 0,
                    'num_votes': 0
                }
            }

        for option in options:
            v = cell.get('votes').get(option, 0)
            data[key]['counts'][option] += v
        
        for k, v in cell.items():
            if k in blocs:
                data[key]['bloc'][k] = v

        data[key]['motion_id'] = cell.get('motion_id')
        data[key]['stats']['num_motions'] += 1
        data[key]['stats']['num_votes'] += cell['num_votes']

    return data.values()
