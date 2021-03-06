from flakon import JsonBlueprint
from flask import request
from kbsbot.compose_engine.compose_utils import *
from kbsbot.compose_engine.services import *
import logging

comp = JsonBlueprint('comp', __name__)

TRAINING_TOOL = "http://example.com/train"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@comp.route('/status', methods=["GET"])
def get_status():
    return {"message": "ok"}


@comp.route('/compose', methods=["GET"])
def compose():
    """
    his view encapsulates the method get_intent_options.
    It requires an Intent.

    :return: A dict containing the answer, the intent an entities found


    .. todo:: Check if entities are null

    .. todo:: Handle when answer has a resource

    """
    data = request.get_json()
    # print(data)
    logger.info(">>>>> Incoming data  %s", data)
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

    if "help" in data and data["help"] is True:
        agent_data = get_agent_data(agent)
        return {"context": {"intent": local_intent, "entities": entities},
                "answer": {"answer_type": "help", "help": agent_data}}

    message = ""
    if local_intent is None:
        # print("Looking for intent")
        if len(user_input) > 0:
            local_intent = discover_intent(agent, user_input)
        # print("Intent found ", local_intent)
        # logger.info("Intent found %s", local_intent)
        if local_intent is None:
            logger.info(">>>>> Intent not found, appending message to unclassified")
            not_intent_msg = f"Lo siento no he podido entener a que te refieres." \
                             f"\nAyudamos a entrenar el chatbot en el siguiente enlace: {TRAINING_TOOL}"
            return {"context": {"intent": None, "entities": [], "classified": False},
                    "answer": {"answer_type": "text", "text": not_intent_msg}}
    if len(entities) == 0:
        # print("Looking for entities")
        entities = discover_entities(agent, user_input)
        # print("Entities found ", entities)
        logger.info("Entities found %s", entities)

    requirements = get_requirements(local_intent)
    # print("Requirements ", requirements)
    logger.info("Requirements  %s", requirements)
    options = False
    missing_entities = None
    if requirements is not None and len(requirements) > 0:
        missing, missing_entities = check_requirements(requirements, entities)
        # print("Missing requirements", missing, " :", missing_entities)
        logger.info("Still Missing requirements  %s  ", missing_entities)
        if missing is True:
            try:
                found_entities = discover_entities(agent, user_input)
            except Exception as e:
                logger.info("Error  %s  ", e)
            else:
                # print("Found entities in text", found_entities)
                logger.info("Found entities in text  %s  ", found_entities)
                missing, missing_entities = check_requirements(requirements, found_entities)
                # print("Missing requirements", missing, " :", missing_entities)
                logger.info("Still Missing requirements  %s  ", missing_entities)
                if missing is False:
                    entities = update_entities(entities, found_entities)

        if missing is True:
            try:
                found_entities = find_in_context(user, missing_entities)
            except Exception as e:
                logger.info("Error  %s  ", e)
            else:
                # print("Found entities in context", found_entities)
                logger.info("Found entities in context  %s  ", found_entities)
                missing, missing_entities = check_requirements(requirements, found_entities)
                # print("Missing requirements", missing, " :", missing_entities)
                logger.info("Still Missing requirements  %s  ", missing_entities)
                if missing is False:
                    entities = update_entities(entities, found_entities)

        if missing is True:
            # print("Still Missing requirements", missing_entities)
            logger.info("Can´t find requirements  %s  ", missing_entities)
            options = True
    else:
        message += "Null requirements"

    resource = False
    options_list = None
    # print("OPTIONS STATUS", options)
    logger.info("OPTIONS STATUS  %s", options)
    if options is True:
        options_list = get_options(missing_entities[0])
        # print("OPTIONS LIST", options_list)
        logger.info("OPTIONS LIST  %s", options_list)
        if len(options_list) == 0:
            return {"context": {"intent": local_intent, "entities": entities, "classified": False},
                    "answer": {"answer_type": answer_type, "text": "No existen opciones, que deseas conocer?"}}
        else:
            answer = {"options": options_list}
            answer_type = "options"
            resolution_question = get_intent_rq(local_intent, options_list["entity"])
            answer["template"] = resolution_question["rq"]
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
    logger.info("ANSWER  %s", answer)
    # print("Answer", answer)
    logger.info("ANSWER  type %s", answer_type)
    print("Answer type", answer_type)

    if resource:
        pass

    final_answer = build_answer(answer, answer_type)
    # print("FINAL ", final_answer)
    resp = {"context": {"intent": local_intent, "entities": entities, "classified": False},
            "answer": final_answer}

    if len(message) > 0:
        resp["message"] = message

    logger.info("<<<<<< FINAL  %s", resp)
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
