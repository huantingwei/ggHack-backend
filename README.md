# ggHack Backend API

## Setup

### Virtual Environment
Recommended to use **python virtualenv** or **conda** to set up a separated environment. Please check
- pip: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
- anaconda: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

### pip install
```python
pip install django
pip install djangorestframework
```

## Run the program
```python
python manage.py runserver
```

## Install PostgreSQL
1. Download Postgres.app
 
- https://postgresapp.com/downloads.html

2. Create local PostgreSQL database
Open Postgres.app, click Start button to run the database server. 
Then click postgres database, and it will show you a terminal window:

```
$ psql
psql (9.3.4)
Type "help" for help.

postgres=#
```

Create a database:
```
postgres=# CREATE DATABASE _name_;
```

3. Installing PostgreSQL package for Python in your project virtual env
```
pip install psycopg2
```
4. Updating Django Project setting 
in ross.settings.py file:
```
    DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'gghack_backend_db',                      
            'USER': 'yihanliao',                     
            'PASSWORD': '',               
            'HOST': "",                           
            'PORT': '5432', # you can check port number at server setting in the postgres.app                    
        }
    }
```

