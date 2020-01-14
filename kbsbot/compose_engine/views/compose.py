from flakon import JsonBlueprint
from flask import request
from kbsbot.compose_engine.utils import *
from kbsbot.compose_engine.services import *

comp = JsonBlueprint('comp', __name__)


@comp.route('/compose')
def compose():
    """
    his view encapsulates the method get_intent_options.
    It requires an Intent.

    :return: A dict containing the answer, the intent an entities found


    .. todo:: if intent is None inform admin.

    .. todo:: Check if entities are null

    .. todo:: Handle when answer has a resource

    .. todo:: check in context

    .. todo:: Get options
    """
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
        print("Intent found ", intent)
        if intent is None:
            pass
    if len(entities) == 0:
        print("Looking for entities")
        entities = discover_entities(agent, user_input)
        print("Entities found ", entities)

    requirements = get_requirements(intent)
    print("Requirements ", requirements)
    options = False
    missing_entities = None
    if len(requirements) > 0:
        missing, missing_entities = check_requirements(requirements, entities)
        print("Missing requirements", missing, " :", missing_entities)

        if missing is True:
            entities = find_in_context(user, agent, channel, missing_entities)

            missing, missing_entities = check_requirements(requirements, entities)
            if missing is True:
                print("Still Missing requirements", missing_entities)
                options = True

    resource = False
    options_list = []
    print("OPTIONS ", options)
    if options is True:
        options_list = get_options(missing_entities)
        answer_type = "options"
    else:
        print("Looking for answer")
        answer = get_answer(intent, entities)

        if "resource" in answer:
            resource = True
        else:
            answer_type = "text"

    print("Answer", answer)

    if resource:
        pass

    final_answer = build_answer(answer, answer_type)
    print("FINAL ", final_answer)
    resp = {"context": {"intent": intent, "entites": entities},
            "answer": {"answer_type": answer_type, "text": final_answer}}
    if len(options_list) > 0:
        resp["answer"]["options"] = options_list
    return resp
