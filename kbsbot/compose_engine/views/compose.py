from flakon import JsonBlueprint
from flask import request
from kbsbot.compose_engine.utils import *
from kbsbot.compose_engine.services import *

comp = JsonBlueprint('comp', __name__)


@comp.route('/compose')
def compose():
    data = request.get_json()
    print(data)
    agent = data["agent"]
    user = data["user"]
    channel = data["channel"]
    answer = None
    answer_type = None
    intent = data["context"]["intent"]
    entities = data["context"]["entities"]
    user_input = data["user_input"]
    if intent is None:
        print("Looking for intent")
        intent = discover_intent(agent, user_input)
        # TODO check if entities are null
    if len(entities) == 0:
        print("Looking for entities")
        entities = discover_entities(agent, user_input)

    requirements = get_requirements(intent)
    context_search = False
    options = False
    resource = False
    while True:
        missing, missing_entities = check_requirements(requirements, entities)
        if missing is False:
            answer = get_answer(intent, entities)
            if "resource" in answer:
                resource = True
            else:
                answer_type = "text"
            break
        else:
            if context_search is False:
                entities = find_in_context(user, agent, channel, missing_entities)
                context_search = True
            else:
                options = True
                break

    if options is True:
        answer = get_options(missing_entities)
        answer_type = "options"

    if resource:
        # TODO handle when answer has a resource
        pass

    final_answer = build_answer(answer, answer_type)
    """
    TODO add all updated info
    intent
    entites
    answer {
    "type":
    "text":
    "options": []
    }
    
    """
    print(final_answer)
    return {"answer": "TODO bien", "answer_type": answer_type}
