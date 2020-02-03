from flakon import JsonBlueprint
from flask import request
from kbsbot.compose_engine.compose_utils import *
from kbsbot.compose_engine.services import *

comp = JsonBlueprint('comp', __name__)


@comp.route('/compose', methods=["GET"])
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
    answer = None
    answer_type = None
    user_input = data["user_input"]
    local_intent = None
    entities = []
    if "context" in data:
        if "intent" in data["context"]:
            local_intent = data["context"]["intent"]
        if "entities" in data["context"]:
            entities = data["context"]["entities"]

    message = ""
    if local_intent is None:
        print("Looking for intent")
        local_intent = discover_intent(agent, user_input)
        print("Intent found ", local_intent)
        if local_intent is None:
            return {"message": "Intent not found"}
    # TODO check and replace entities
    if len(entities) == 0:
        print("Looking for entities")
        entities = discover_entities(agent, user_input)
        print("Entities found ", entities)

    requirements = get_requirements(local_intent)
    print("Requirements ", requirements)
    options = False
    missing_entities = None
    if requirements is not None:
        if len(requirements) > 0:
            missing, missing_entities = check_requirements(requirements, entities)
            print("Missing requirements", missing, " :", missing_entities)
            if missing is True:
                found_entities = find_in_context(user, missing_entities)
                print("Found entities in context", found_entities["entities"])
                missing, missing_entities = check_requirements(requirements, found_entities["entities"])
                if missing is True:
                    print("Still Missing requirements", missing_entities)
                    options = True
                else:
                    entities = found_entities
    else:
        message += "Null requirements"

    resource = False
    options_list = None
    print("OPTIONS STATUS", options)
    if options is True:
        options_list = get_options(missing_entities[0])
        print("OPTIONS LIST", options_list)
        if len(options_list) == 0:
            return {"message": "Must configure options to resolve entity", "status": 404}
        else:
            answer = {"options": options_list}
            answer_type = "options"
    else:
        print("Looking for answer")
        print(local_intent, entities)
        answer = get_answer(local_intent, entities)
        if answer is not None:
            if "resource" in answer:
                resource = True
            else:
                answer_type = "text"
        else:
            message += "Null requirements"

    # if "status" in answer:
    #     return answer

    print("Answer", answer)
    print("Answer type", answer_type)

    if resource:
        pass

    final_answer = build_answer(answer, answer_type)
    print("FINAL ", final_answer)
    resp = {"context": {"intent": local_intent, "entities": entities},
            "answer": {"answer_type": answer_type, "text": final_answer}}
    if options_list is not None:
        resp["answer"]["options"] = options_list
    if len(message) > 0:
        resp["message"] = message
    return resp


@comp.route('/test/intent', methods=["GET"])
def get_intent_view():
    data = request.get_json()
    agent = data["agent"]
    user_input = data["user_input"]
    intent_found = discover_intent(agent, user_input)
    return {"intent": intent_found}


@comp.route('/test/requires', methods=["GET"])
def get_requirements_view():
    data = request.get_json()
    local_intent = data["context"]["intent"]
    requires = get_requirements(local_intent)
    return {"requires": requires}


@comp.route('/test/answer', methods=["GET"])
def get_answer_view():
    data = request.get_json()
    agent = data["agent"]
    user_input = data["user_input"]
    entities = discover_entities(agent, user_input)
    local_intent = discover_intent(agent, user_input)
    result = get_answer(local_intent, entities)
    return {"result": result, "entities": entities, "intent": local_intent}
