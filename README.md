# County Farmers, Produce and Sales management software

To run project, run the following commands in the project's directory to create the database. When running the software for the first time, it is necessary 
After the first time, the following can be run to migrate model changes in any app
```
python manage.py makemigrations
python manage.py migrate
```
Use the following command to create an admin user 
```
python manage.py createsuperuser
```

Use the following command to run the server(start the system locally)
```
python manage.py runserver
```
accessing the system
```
visit: http://localhost:8000/ on your browser
```
