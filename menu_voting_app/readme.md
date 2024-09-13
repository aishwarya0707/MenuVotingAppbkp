## Project overview

### About

Company needs internal service for its’ employees which helps them to make a decision
on lunch place.

Each restaurant will be uploading menus using the system every day over API
Employees will vote for menu before leaving for lunch on mobile app for whom backend has to be implemented
There are users which did not update app to the latest version and backend has to support both versions.
Mobile app always sends build version in headers.

### Needed API’s:

o Authentication
o Creating restaurant
o Uploading menu for restaurant (There should be a menu for each day)
o Creating employee
o Getting current day menu
o Voting for restaurant menu (Old version api accepted one menu, New one accepts top three menus with respective points (1 to 3))
o Getting results for current day

### Requirements:

Solution should be built using Python and preferably Django Rest Framework, but any other framework works
App should be containerised
Project and API Documentation
• Tests

### Extra points

HA Cloud Architecture Schema/Diagram (Preferably Azure)
Usage of Linting and Static typing tools

# Project structure

The project is divided into 2 smaller apps. They are
• users - Contains logic related to User login, logout, register, employee creation
• restaurants - Contains logic related to restaurants, voting and menus

### MODELS:

Restaurant
Menu
Vote
Employee

### END POINTS:

- Create a restaurant --> /restaurants/create-restaurant/
- Uploading menu for restaurant --> /restaurants/upload-menu/
- vote for restaurant menu using old version api or new version api --> /restaurants/restaurant-votes/
- Getting results for current day --> /restaurants/current-day-menus/
- New users can be registered --> /users/register/
- Users can login --> /users/login/
- Users can logout --> /users/logout/
- Employee can be created --> /users/create-employee/

### API Usage for Users:

https://www.postman.com/technical-cosmologist-79820612/workspace/menuvotingapp/collection/18019390-de270b15-7ff0-424d-bc4d-76227b7e3f38?action=share&creator=18019390

### API Usage for Restaurants:

https://www.postman.com/technical-cosmologist-79820612/workspace/menuvotingapp/collection/18019390-06055f31-652d-435a-97c8-61c1bdf713a2?action=share&creator=18019390

## To run development server

Follow the below steps

- Move the virtual environment and activate it

`cd .\env\Scripts\`
`.\activate`

- Create super user
  `cd ..`
  `cd .\menu_voting_app\`
  `python manage.py createsuperuser`

- Run the server

`python manage.py runserver`

- Run tests

`coverage run manage.py test`

# Build the Docker image

docker-compose build

# Run the Docker containers

docker-compose up

# Run the Docker containers in detached mode

runserver-detached:
docker-compose up -d

# Stop the Docker containers

down:
docker-compose down

# Restart the Docker containers

restart:
docker-compose restart

# Access the Django shell

docker-compose run web python manage.py shell

# Apply database migrations

docker-compose run web python manage.py makemigrations

# Apply database migrations

docker-compose run web python manage.py migrate

# Run tests

test:
docker-compose run web python manage.py test

# Generate code coverage report

docker-compose run web coverage run --source='.' manage.py test
docker-compose run web coverage report

# createsuperuser:

docker-compose run --rm web ./manage.py createsuperuser

# To fix linting

docker-compose run --rm web black .

# To static typing

docker-compose run --rm web isort .
