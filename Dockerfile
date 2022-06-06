FROM python:3.10.4-alpine3.16
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /django/requirements.txt
WORKDIR /django
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && \
    pip install --upgrade pip && pip install -r requirements.txt

COPY . /django
ENTRYPOINT [ "sh", "entrypoint.sh" ]