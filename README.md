# Scaffolding
A scaffolding for a Flask project.

## Requirements
- Python 3.7.x
- Redis 5.0.x

## Bootstrap
    $ make bootstrap

## Run
    $ ./run.py
Accessible at: `http://localhost:5000`

## Deploy
### Create
    $ make deploy
### Remove
    $ make teardown

## Usage
### Endpoints
Accessible at: `http://localhost`

Method | Path | Query String / Body | Request Headers | Status Codes
--- | --- | --- | --- | ---
GET | `/resources/<resource_id>` | | Authorization=Bearer <ACCESS_TOKEN> Accept=application/v<SEM_VER>+json | 200, 401, 403, 404, 406, 500
POST | `/resources` | { id:, value: } | Authorization=Bearer <FRESH_ACCESS_TOKEN> Content-Type=application/v<SEM_VER>+json | 200, 400, 401, 403, 406, 409, 500
POST | `/login` | { username:, password: } | | 200, 400, 500
POST | `/refresh` | | Authorization=Bearer <REFRESH_TOKEN> | 200, 500
POST | `/fresh-login` | { username:, password: } | | 200, 400, 500
