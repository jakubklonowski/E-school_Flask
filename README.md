# E-platform for school

## Author
Author of this app is Jakub Klonowski (jakubpklonowski@gmail.com).

## Description
The app is e-platform for school. Users can publish and read news and grades. 
In future releases more features will be supported.

## Functionalities:
- registration, login, sessions;
- different levels of user permissions;
- creating and reading data from database (CR of CRUD).

## Technologies
Project was coded in CPython language and uses SQLite database.

Full list of used technologies:
- CPython 3.10.6
- SQLite 2.6.0
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

## Development ideas
- changes in database structure;
- full CRUD support for existing data sources;
- different languages support.