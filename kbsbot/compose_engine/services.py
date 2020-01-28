from requests import Session
import requests
import os

# NLP_ENGINE_URL = "http://127.0.0.1:5001"
# INTENTS_MANAGMENT_URL = "http://127.0.0.1:5002"
# CONTEXT_MANAGMENT_URL = "http://127.0.0.1:5003"

NLP_ENGINE_URL = os.environ.get('NLP_ENGINE_URL')
INTENTS_MANAGMENT_URL = os.environ.get('INTENTS_MANAGMENT_URL')
CONTEXT_MANAGMENT_URL = os.environ.get('CONTEXT_MANAGMENT_URL')

session = Session()
session.trust_env = False
session.verify = False
session.headers["Accept"] = "application/json"
session.headers["Content-Type"] = "application/json"


def discover_intent(agent, text):
    """
    This method connects to the microservice *NLP Engine* in order to retrieve the intents from a raw text.

    :param agent: The agent name of the chatbot

    :param text: The raw input to discover the intent

    :return: The uri of a intent
    """
    url = NLP_ENGINE_URL + "/intents"
    try:
        r = session.get(url, json={"agent": agent, "sentence": text})
        if r.status_code == 200:
            response = r.json()
            return response["intent"][0]["prediction"]
    except requests.exceptions.RequestException as e:
        print(e)


def discover_entities(agent, text):
    """
        This method connects to the microservice *NLP Engine* in order to retrieve the entities from a raw text.

        :param agent: The agent name of the chatbot

        :param text: The raw input to discover the intent

        :return: A list with the URIS of the entities and type of entities.
    """
    url = NLP_ENGINE_URL + "/entities"
    try:
        r = session.get(url, json={"agent": agent, "sentence": text})
        if r.status_code == 200:
            response = r.json()
            entities = []

            for entity in response["entities"]:
                entities.append({
                    "type": entity["entity"],
                    "value": entity["prediction"],
                })
            return entities
    except requests.exceptions.RequestException as e:
        print(e)


def get_requirements(intent):
    """
    This service connects to the microservice *Intents Managment* in order to retrieve requirements of an intent

    :param intent: The intent from where requirements will be retrieved

    :return: A list of URIS of the different entities needed to complete an intent
    """
    url = INTENTS_MANAGMENT_URL + "/intent/requires"
    try:
        r = session.get(url, json={"intent": intent})
        if r.status_code == 200:
            response = r.json()
            if "requires" in response:
                return response["requires"]
            else:
                return None
    except requests.exceptions.RequestException as e:
        print(e)


def get_options(entity):
    """
        This service connects to the microservice *Intents Management* in order to retrieve options of an entity type

        :param entity: The entity from where options will be retrieved

        :return: A list of options to complete an entity

        .. todo:: give a list of entities
        """
    url = INTENTS_MANAGMENT_URL + "/entity/options"
    try:
        print({"entity": entity})
        r = session.get(url, json={"entity": entity})
        if r.status_code == 200:
            response = r.json()
            return response["options"]

    except requests.exceptions.RequestException as e:
        print(e)


def find_in_context(user, agent, channel, entities):
    return []


def get_answer(intent, entities):
    """
            This service connects to the microservice *Intents Management* in order to retrieve the answer of an intent.

            :param intent: The intent from where answer will be retrieved

            :param entities: A list of entities used to retrieve answer

            :return: A list of options to complete an entity
            """
    url = INTENTS_MANAGMENT_URL + "/intent/answer"
    try:
        r = session.get(url, json={"intent": intent, "entities": entities})
        if r.status_code == 200:
            response = r.json()
            return response
    except requests.exceptions.RequestException as e:
        print(e)
