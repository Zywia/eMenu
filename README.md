## Installation

### first steps
1. docker-compose build
2. docker-compose up

### In new terminal
1. go to project directory   
2. docker-compose exec web bash
3. cd eMenu 
4. python manage.py migrate
5. python manage.py makemigrations
6. python populate.py
7. python -m smtpd -n -c DebuggingServer localhost:587

### In next new terminal
1. go to project directory   
2. docker-compose exec web bash
3. cd eMenu
4. celery -A eMenu worker -B


## To run tests and check coverage
1. open terminal in project directory
2. docker-compose exec web bash
3. cd eMenu
4. python manage.py menuCard.tests
5. coverage run --source='.' manage.py test menuCard.tests
6. coverage report


## Swagger path
http://0.0.0.0:8000/api/schema/swagger-ui/

## superuser credentials:
- username: admin
- password: admin
