# ggHack Backend API

## Setup

### Create virtual environment
*It is recommended to create a virtual environment before doing the following procedures*  
Use **python virtualenv** or **conda** to set up a separated environment. Please check
- pip: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
- anaconda: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

### Install dependencies
```python
pip install -r requirements.txt
```


### Install PostgreSQL
1. Download Postgres.app
 
   https://postgresapp.com/downloads.html

2. Create local PostgreSQL database
   - Open Postgres.app, click Start button to run the database server. 
   - Then click postgres database, and it will show you a terminal window:
  

   ![image] (https://github.com/huantingwei/ggHack-backend/blob/master/backend/images/postgre_app.png)


   ```
   $ psql
   psql (9.3.4)
   Type "help" for help.

   postgres=#
   postgres=# CREATE DATABASE YOUR_DATABASE_NAME;
   ```

3. Update Django project database setting 
in **ross/settings.py** file:
   ```
       DATABASES = {
           'default':{
               'ENGINE': 'django.db.backends.postgresql_psycopg2', 
               'NAME': 'YOUR_DATABASE_NAME',                      
               'USER': 'YOUR_USER_NAME',                     
               'PASSWORD': 'YOUR_PASSWORD',               
               'HOST': "YOUR_HOSTNAME", # "" for localhost                           
               'PORT': 'YOUR_PORT_NUMBER(5432)', # you can check port number at server setting in the postgres.app                    
           }
       }
   ```


## Run the program
```python
python manage.py runserver
```
