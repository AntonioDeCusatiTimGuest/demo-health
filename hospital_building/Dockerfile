FROM python:3.8-alpine as base

FROM base as builder

RUN mkdir /install && apk add --no-cache python3-dev openssl-dev libffi-dev libc-dev gcc geos-dev g++

WORKDIR /install

COPY requirements.txt /requirements.txt

RUN export PATH="${PATH}:/install/bin"; \
    export PYTHONPATH="${PYTHONPATH}:/install/bin"; \
    pip3 install --upgrade pip; \
    pip3 install --prefix=/install -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local

COPY src /app

WORKDIR /app

RUN chown 1000:1000 -R /app

USER 1000

# CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "main:app"]
CMD ["python3", "main.py"]