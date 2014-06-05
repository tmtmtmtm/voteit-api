# VoteIt API Server

This is a server component for a VoteIt API — part of a suite of tools for managing parliamentary (or other) vote results. 

## Installation 

Before installing, make sure you have the following dependencies available on your system:

* MongoDB, ideally greater than 2.7.
* Python 2.7 and [virtualenv](http://www.virtualenv.org/en/latest/)

When you set up  ``voteit-api``, first check out the application from GitHub,
create a virtual environment and install the Python dependencies:

    git clone https://github.com/tmtmtmtm/voteit-api.git
    cd voteit-api
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py develop

Next, you need to start MongoDB. For testing, you can simply run

    mongod --dbpath=/tmp

You also need to configure ``voteit-api`` to point at this. Create a copy of the file ``voteit/default_settings.py``, as ``settings.py`` in the repository base, and change ``MONGODB_URI`` if required (the default should just work unless you've configured MongoDB differently).

Once the new configuration is set up, you need to set an environment variable to point ``voteit-api`` at the configuration file:

    export VOTEIT_SETTINGS=`pwd`/settings.py

Finally, you can run ``voteit-api``. 

    python voteit/manage.py runserver 

Test that it's working by visiting the URL it tells you it's running on. 

## Day-to-day Development

When developing voteit-api day-to-day, you'll need to run

    source env/bin/activate

whenever you start a new shell. This tells Python to load the dependencies for
voteit-api. It will place `(env)` at the start of your shell prompt.

## Bulk loader format

Data for people, parties, and votes, conforming to the relevant [Popolo specfications](http://popoloproject.com/specs/vote-event.html), can be bulk-loaded from JSON files. 

* ``people.json`` - Popolo person data for each person that has cast votes. ([Example](https://github.com/tmtmtmtm/eduskunta-popolo/blob/master/people.json))
* ``parties.json`` - Popolo organization data for each person that has cast votes. ([Example](https://github.com/tmtmtmtm/eduskunta-popolo/blob/master/parties.json))
* ``motions.json`` - Popolo motion data, with nested vote_events, vote_counts, and votes. ([Example](https://github.com/tmtmtmtm/eduskunta-popolo/blob/master/data/popolo/2012/session-100.json))

Each ``vote`` is expected to contain a ``party_id`` and ``voter_id`` that resolve against the people and party data.

These files can be imported using:

    python voteit/manage.py loadpeople <filename>
    python voteit/manage.py loadparties <filename>
    python voteit/manage.py loadmotions <filename>

It is presumed that your normal usage is 'append only' — i.e. that
historic data will not change — you will simply be adding new data. As
such these do bulk imports, and so will not replace or ignore
pre-existing records, but issue an error if clashes are detected.

If you do need to change historic data, you can either write your own
code to do that, or simply delete and recreate any data set (for
the average Parliament, a complete `people.json` file will reload in
a few seconds)

To clean out existing data first you can run:

    python voteit/manage.py deletepeople
    python voteit/manage.py deleteparties
    python voteit/manage.py deletemotions

or all three at once:

    python voteit/manage.py deletealldata

## API Documentation

A read-only API exposes the following end-points:
 
* GET /api/1/motions
* GET /api/1/motion/`<motion_id>`
* GET /api/1/vote_events
* GET /api/1/vote_events/`<vote_event_id>`
* GET /api/1/parties
* GET /api/1/parties/`<party_id>`
* GET /api/1/persons
* GET /api/1/persons/`<party_id>`

An `aggregrate` API end-point is also provided that allows grouping and filtering of vote information. For example:

To see vote counts by party on a given motion:
*  GET /api/1/aggregate?motion=62-2012-1&bloc=party_id
  
Or how a specific party voted on a range of motions:
*  GET /api/1/aggregate?motion=62-2012-1&motion=62-2012-2&filter=party_id:13
  
