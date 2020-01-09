from flakon import JsonBlueprint
from flask import request

comp = JsonBlueprint('comp', __name__)


@comp.route('/compose')
def compose():
    data = request.get_json()
    print(data)
    return {"message":"TODO bien"}


