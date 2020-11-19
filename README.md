Backend webdev test project 2020-10
===
Example setup of simple Django web app with REST API & Ajax-handler:
- ORM setup with admin;
- simple view for authorized users;
- some async visualization in plain JS;
- simple Docker config for development.

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

3) Add URLs via Django admin panel:

`http://0.0.0.0:8000/admin`

4) The list of URLs will be displayed on home page, red/green showing connectivity status (NOT a11y-friendly):

`http://0.0.0.0:8000/`