from requests import Session
import os


NLP_ENGINE_URL = os.environ.get('NLP_ENGINE_URL')
INTENTS_MANAGMENT_URL = os.environ.get('INTENTS_MANAGMENT_URL')
CONTEXT_MANAGMENT_URL = os.environ.get('CONTEXT_MANAGMENT_URL')

session = Session()
session.trust_env = False
session.verify = False
session.headers["Accept"] = "application/json"
session.headers["Content-Type"] = "application/json"
proxies = {
    "http": None,
    "https": None,
}


def discover_intent(agent, text):
    url = NLP_ENGINE_URL + "/intents"
    print(url)
    r = session.post(url, json={"agent": agent, "text": text})
    if r.status_code == 200:
        response = r.json()
        intent = {
            "label": response[0]["intent"]["label"],
            "probability": response[0]["intent"]["probability"]
        }
        return intent
        # return response["label"]
    else:
        return None


# discover_intent("opencampuscursos", "Que cursos hay")


def discover_entities(agent, text):
    pass


def get_requirements(intent):
    pass


def get_options(entity):
    pass


def find_in_context(user, agent, channel, entities):
    pass


def get_answer(intent, entities):
    pass
