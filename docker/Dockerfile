FROM python:3.7

RUN pip install gunicorn

COPY docker/settings.ini /app/kbsbot/compose_engine/settings.ini

COPY . /app

RUN pip install -r /app/requirements.txt
RUN pip install /app/

ENV NLP_ENGINE_URL="http://0.0.0.0:8001"
ENV INTENTS_MANAGMENT_URL="http://0.0.0.0:8002"
ENV CONTEXT_MANAGMENT_URL="http://0.0.0.0:8006"

WORKDIR /app/kbsbot/compose_engine
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app"]