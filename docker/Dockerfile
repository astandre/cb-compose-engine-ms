FROM python:3.7

RUN pip install gunicorn

COPY docker/settings.ini /app/settings.ini

COPY . /app

RUN pip install -r /app/requirements.txt
RUN pip install /app/

EXPOSE 8001
CMD ["gunicorn", "-b", "0.0.0.0:8001", "compose-engine", "--config-file", "./app/settings.ini", "-d"]






