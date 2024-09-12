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
o Voting for restaurant menu (Old version api accepted one menu, New one accepts top three menus with respective points (1 to 3)
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

To ensure reusability, modularity and ease to expanding the codebase the project is divided into three smaller apps.

The three modules/apps in this project:

• user_profiles - logic realted to authentication, employee creation
• restaurants - logic related to restaurants and menus
• votes - logic related to voting

### User profiles

### Models:

UserProfile
Employee
Role
Organization

### About

- New users can be registered
- Handles authentication - login, logout using TokenAuthentication
- Employee can be created
- Organisation can be created which is used by employee model
- Role/designation of an employee can be added

Please refer to the API documentation for more details - [User Profile API collection](https://web.postman.co/workspace/8b70aae8-9083-4850-84da-03ed46ce1dc3/api/e2f08a5d-7234-4107-b611-92825c2f102f/documentation/4100828-2f17873e-4d7d-4756-b87c-03e02fe0b276?entity=&branch=&version=)

### Restaurants

### Models:

Restaurant
Menu

### About

- Create a restaurant
- List restaurants
- Upload menu for restaurant
- Update vote for menu which is done by the votes api

Please refer to the API documentation for more usage info - [Restaurant API collection](https://web.postman.co/workspace/8b70aae8-9083-4850-84da-03ed46ce1dc3/api/e2f08a5d-7234-4107-b611-92825c2f102f/collection/4100828-822be501-90b8-460a-a243-6d2effd761c8)

### Votes

#### Models

Vote

### About

- Creates the relation between the user profile and restaurants module
- The model maps votes to Employee and Menu

Please refer to the API documentaion - [Vote API collection](https://web.postman.co/workspace/8b70aae8-9083-4850-84da-03ed46ce1dc3/api/e2f08a5d-7234-4107-b611-92825c2f102f/documentation/4100828-c95738f9-33e6-4fa3-ba37-50cdf069e985?entity=&branch=&version=)

## Running the project

To make running the docker django commands easier a Makefile has been added which has the following commands

- `make setup` -Sets up the project: runs build and migrate

- `make build` - Runs docker-compose build

- `make runserver` - Runs the command docker-compose up

- `make makemigrations` - Runs ./manage.py makemigrations

- `make migrate` - Runs ./manage.py migrate

- `make fix-linting` - Prettifies the codebase by running `black .` , `isort .`

There are few more commands added to the Makefile which could be run using the keyword provided before every command

## To run development server

Follow the below steps

- Setup the project

`make setup`

- Create super user

`make createsuperuser`

- Run the project

`make runserver`

- Run tests

`make test`
