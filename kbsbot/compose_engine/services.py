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
            if "intent" in response and len(response["intent"]) > 0:
                return response["intent"][0]["prediction"]
            else:
                return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None


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
        return []


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
        return None


def get_options(entity):
    """
        This service connects to the microservice *Intents Management* in order to retrieve options of an entity type

        :param entity: The entity from where options will be retrieved

        :return: A list of options to complete an entity

        .. todo:: give a list of entities
        """
    url = INTENTS_MANAGMENT_URL + "/entity/options"
    try:
        # print({"entity": entity})
        r = session.get(url, json={"entity": entity})
        if r.status_code == 200:
            response = r.json()
            return response

    except requests.exceptions.RequestException as e:
        print(e)
        return None


def find_in_context(user, entities):
    """
    This method looks for information in the conversation thread.
     :param user: The id of the user to find information

     :param entities: The entities to be found in context.
    """
    url = CONTEXT_MANAGMENT_URL + "/context/entities"
    try:
        r = session.get(url, json={"user": user, "entities": entities})
        if r.status_code == 200:
            response = r.json()
            if "entities" in response:
                entities = response["entities"]
                return entities
            else:
                return []
    except requests.exceptions.RequestException as e:
        print(e)
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


def get_agent_data(agent):
    """
        This service connects to the microservice *Intents Management* in order to information about and agent

        :param agent: A valid agent name

        :return: A dict containing agent, a description and the different intents.

        """
    url = INTENTS_MANAGMENT_URL + "/agent/info"
    try:
        r = session.get(url, json={"agent": agent})
        if r.status_code == 200:
            response = r.json()
            return response

    except requests.exceptions.RequestException as e:
        print(e)
        return None


def get_intent_rq(intent, entity):
    """
        This service connects to the microservice *Intents Management* in order to get the resolution question of an intent

        :param intent: A valid intent

        :param entity: A valid entity

        :return: A dict containing intent, a entity and the resolution question.

        """
    url = INTENTS_MANAGMENT_URL + "/intent/rq"
    try:
        r = session.get(url, json={"intent": intent, "entity": entity})
        if r.status_code == 200:
            response = r.json()
            return response

    except requests.exceptions.RequestException as e:
        print(e)
        return None
