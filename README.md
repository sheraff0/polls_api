Backend webdev test project 2020-11
===
Example setup of __Polls__ Django web app with REST API:
- models, serializers, viewsets, API urls setup;
- authorized admin endpoints with full access;
- anon-friendly user endpoints with access to polls.

Running in local environment:
-
1) In project root, create `.env` file with:
`SECRET_KEY=<key>`
and optionally `DB_NAME`, `DB_USER`, `DB_PASSWORD` variables.

2) Build and run docker image:

`docker-compose build`

`docker-compose run web python manage.py migrate`

`docker-compose run web python manage.py createsuperuser`

`docker-compose up`

3) Hence, ready to accept connections at:

`http://0.0.0.0:8000/<api_url>`

API entry points:
-
-  __/api/__ - common root;
	-  __/polls/__, __/options/__, __/questions/__, __/respondents/__, __/answers/__ - respective endpoints with a standard set of REST methods (GET, POST, PUT, PATCH, DELETE), available to _admin_ user, via auth-token provided in header:
`-H 'Authorization: token <token>'`
-  __/auth/__ - auth root;
    - sample request to obtain auth token:
`curl -X POST '0.0.0.0:8000/auth/' \`
`-H 'Content-Type: application/json' \`
`-d '{"username": "<username>", "password": "<password>"}'`


User endpoints (no auth token required):
-  __/api/polls/active-list/__ - get available polls to current date;
-  __/api/polls/<id>/get-poll/__ - get complete layout of specified poll;
-  __/api/respondents/add-respondent/__ - (POST) add respondent; returns created respondent object with UUID:
`curl -X POST '0.0.0.0:8000/api/respondents/add-respondent/' \`
`-H 'Content-Type: application/json' -d '{"name": "<respondent name (optionally)>"}'`
-  __/api/respondents/<uuid>/add-poll/__ - (POST) add poll to specified user's list:
`curl -X POST '0.0.0.0:8000/api/respondents/<uuid>/add-poll/' \`
`-H 'Content-Type: application/json' -d '{"poll_id": <poll_id>}'`
-  __/api/respondents/<uuid>/get-polls/__ - get polls from user's list with complete layout and user's answers;
-  __/api/answers/add-answer/__ - (POST) add answer of a user to a question, specified if posted data:
`curl -X POST '0.0.0.0:8000/api/answers/add-answer/' \`
`-d '{"question_id": <question_id>, "respondent_id": "<respondent uuid>", "text": "<text>", "options": [<option_id_1>, <option_id_2>]}' \`
`-H 'Content-Type: application/json'`
returns error message if the is any inconsistency in respondent or question ID's, or in answer types.