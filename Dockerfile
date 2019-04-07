FROM jfloff/alpine-python:3.6 as base


# create a bootstrapped environment
FROM base as environment

WORKDIR /flask-scaffolding

COPY requirements.txt requirements.txt
COPY Makefile Makefile

RUN make bootstrap


# create a distributable package
FROM environment as builder

COPY . .

RUN make build


# install app
FROM environment

COPY --from=builder /flask-scaffolding/dist dist

RUN make install

CMD gunicorn -b 0.0.0.0:$PORT -k gevent -w 2 scaffolding.server:APP
