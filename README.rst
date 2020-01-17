Compose-Engine
==============
.. image:: https://travis-ci.org/astandre/cb-compose-engine-ms.svg?branch=master
    :target: https://travis-ci.org/astandre/cb-compose-engine-ms

.. image:: https://readthedocs.org/projects/cb-compose-engine-ms/badge/?version=latest
    :target: https://cb-compose-engine-ms.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This microservice is  intended to communicate with other services in order to determine intents and entities to retrieve the answer for the channel.


This project is part of the architecture described in:
Herrera, Andre & Yaguachi, Lady & Piedra, Nelson. (2019). Building Conversational Interface for Customer Support Applied to Open Campus an Open Online Course Provider. 11-13. 10.1109/ICALT.2019.00011.




Running scripts


``docker build -t astandre/kbsbot_compose_engine . -f docker/Dockerfile``


``docker run --rm  --name=compose-engine -p 5000:8000 -it astandre/kbsbot_compose_engine``
