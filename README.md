# Django-Recipe_App_REST_API
This is a REST API made using Django,Django REST Framework(DRF),Docker and Test Driven Develoment(TDD).

## Some of the features of this API/project are :~

* Setup the project using Docker.

* Configured Travis-CI for automation of tests.

* Created custom user model so that users can login using their email instead of their username.

* Created endpoints for managing users,recipes,lists,tags and ingredients.

* Used PostgreSQL database.

* Added listing and filtering to the endpoints and well as upload images functionality.

* Followed Test Driven Development(TDD) in which i had to write unit tests first and then the code to make the tests pass.


## How to setup and run this api

* As i have setup the project using Docker so there is not much difficulty on how to set up the project, make sure you have Docker installed on your system.

* Just go the project directory and enter command :~ `sudo docker-compose build`  This will build the docker image used to run the project.

* To check if all the tests are working just enter the command :~ `sudo docker-compose run --rm project sh -c "python manage.py test"

* All tests should pass and then we can start the server using simply :~ `sudo docker-compose up`

* Once the server starts go to `http://127.0.0.1:8000/api/<endpoint>` and the endpoint you wanna check.

* For authenticaing yourself as the user after creating your account use mod header extension or any other extension to store the token and authenticate yourself.

* You can create the superuser simply `sudo docker-compose run --rm project sh -c "python manage.py createsuperuser"`


## Some Blogs i wrote while creating this API

* [Test Driven Development(TDD)](https://medium.com/@ksarthak4ever/test-driven-development-tdd-in-django-and-django-rest-framework-drf-a889a8068cb7)


