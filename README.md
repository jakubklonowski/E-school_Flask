# E-platform for school
## Author
Author of this app is Jakub Klonowski (jakubpklonowski@gmail.com).

## Description
The app is e-platform for school. Three types of users exist within the app: guest, student, teacher. 

## Functionalities
- registration, login, sessions;
- different levels of user permissions;
- full CRUD support;
- logging data to file.

## Technologies
Project was coded in Python language and uses SQLite database.

Full list of used technologies:
- CPython 3.10.6
- SQLite 2.6.0
- HTML5, CSS3, bootstrap5
- WTForms 3.0.1
- Flask 2.2.2
- Werkzeug 2.2.2
- alembic 1.8.1
- SQLAlchemy 1.4.41

Used libraries are in *requirements.txt* file as well.

## Installation
### Database initialization
Use following commands in your terminal:

    flask db init
    flask db migrate
    flask db upgrade

Database **will not** be populated.

## Development ideas
- RWD;
- aria;
- different UI languages support.