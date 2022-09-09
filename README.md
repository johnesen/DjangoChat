# DjangoChat

--- 

1. Clone the repo
   ```sh
   git clone https://github.com/nurj0hn/DjangoChat.git
   ```
2. Create virtual environment with `pipenv`
   ```sh
   pipenv shell
   ```
   
   and install requirements
   ```sh
   pipenv install
   ````
  
3. Create `.env` file in src/
   ```.env
   SECRET_KEY=<secret_key>
   DB_NAME=<db_user>
   DB_USER=<db_user>
   DB_PASSWORD=<db-pswd>
   DB_HOST=<db-host>
   DB_PORT=<int>
   PRODUCTION=<bool>
   DEBUG=<bool>
   CORS_ALLOWED_ORIGINS=<host>
   ALLOWED_HOSTS=<host>
   ```
   
   
   if ```PRODUCTION=True```
      run ``` docker-compose up --build ```
    
   if ```PRODUCTION=False``` run next commands
   
      ```sh
      python src/manage.py makemigrations 
      python src/manage.py migrate  
      python src/manage.py runserver 
      ```
