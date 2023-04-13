FROM python:3.10-alpine

# RUN apk update && apk upgrade
# RUN pip install -U pip poetry==1.1.13

WORKDIR /app

COPY wsgi.py wsgi.py
COPY blog ./blog
COPY migrations ./migrations
COPY requirements.txt .
# COPY poetry.lock .
# COPY pyproject.toml .

# RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt
RUN flask db upgrade

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD ["wsgi.py"]

