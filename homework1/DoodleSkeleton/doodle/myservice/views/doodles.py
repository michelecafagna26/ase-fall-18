from flakon import JsonBlueprint
from flask import request, jsonify, abort
from myservice.classes.poll import Poll, NonExistingOptionException, UserAlreadyVotedException

doodles = JsonBlueprint('/doodles', __name__)

_ACTIVEPOLLS = {} # list of created polls
_POLLNUMBER = 0 # index of the last created poll

@doodles.route('/doodles', methods=['POST', 'GET']) #TODO: complete the decoration
def all_polls():
    if request.method == 'POST':
        result = create_doodle(request)

    elif request.method == 'GET':
        result = get_all_doodles(request)

    return result


@doodles.route('/doodles/<int:id>', methods=['GET', 'DELETE', 'PUT']) #TODO: complete the decoration
def single_poll(id):
    global _ACTIVEPOLLS
    result = ""

    exist_poll(id) # check if the Doodle is an existing one

    if request.method == 'GET': # retrieve a poll
        result = jsonify(_ACTIVEPOLLS[id].serialize())

    elif request.method == 'DELETE':
        #TODO: delete a poll and get back winners
        result = jsonify({'winners':_ACTIVEPOLLS[id].get_winners()})
        del _ACTIVEPOLLS[id]

    elif request.method == 'PUT':
        #TODO: vote in a poll
        result = jsonify({'winners':vote(id, request)})

    return result

@doodles.route('/doodles/<int:id>/<string:person>', methods = ['GET', 'DELETE']) #TODO: complete the decoration
def person_poll(id, person):

    #TODO: check if the Doodle exists
    exist_poll(id) # check if the Doodle is an existing one

    if request.method == 'GET':
        #TODO: retrieve all preferences cast from <person> in poll <id>
        result =jsonify({'votedoptions': _ACTIVEPOLLS[id].get_voted_options(person)})

    if request.method == 'DELETE':
        #TODO: delete all preferences cast from <person> in poll <id>
        result =jsonify({'removed': _ACTIVEPOLLS[id].delete_voted_options(person)})

    return result


def vote(id, request):
    result = ""
    #TODO: extract person and option fields from the JSON request
    json = request.get_json()
    try:
        # TODO: cast a vote from person in  _ACTIVEPOLLS[id]
        result = _ACTIVEPOLLS[id].vote(json['person'], json['option'])
    except UserAlreadyVotedException:
        abort(400) # Bad Request
    except NonExistingOptionException:
        # TODO: manage the NonExistingOptionException
        abort(400) # Bad Request
    return result


def create_doodle(request):
    global _ACTIVEPOLLS, _POLLNUMBER
    #TODO: create a new poll in _ACTIVEPOLLS based on the input JSON. Update _POLLNUMBER by incrementing it.
    json = request.get_json()
    _POLLNUMBER += 1
    _ACTIVEPOLLS[_POLLNUMBER] = Poll(_POLLNUMBER, json['title'], json['options'])

    return jsonify({'pollnumber': _POLLNUMBER})


def get_all_doodles(request):
    global _ACTIVEPOLLS
    return jsonify(activepolls = [e.serialize() for e in _ACTIVEPOLLS.values()])

def exist_poll(id):
    if int(id) > _POLLNUMBER:
        abort(404) # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not(id in _ACTIVEPOLLS):
        abort(410) # error 410: Gone, i.e. it existed but it's not there anymore
