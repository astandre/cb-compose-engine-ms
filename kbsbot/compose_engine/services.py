import requests
from decouple import config

r = requests.get('https://api.github.com/events')
r.json()

NLP_ENGINE_URL = config("NLP_ENGINE_URL")
INTENTS_MANAGMENT_URL = config("INTENTS_MANAGMENT_URL")
CONTEXT_MANAGMENT_URL = config("CONTEXT_MANAGMENT_URL")


def discover_intent(agent, text):
    pass


def discover_entities(agent, text):
    pass


def get_requirements(intent):
    pass


def get_options(entity):
    pass
