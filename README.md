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
   DEBUG=<bool>
   ALLOWED_HOSTS=<host>
   ```
   
   
   than run next commands
      ```sh
      python src/manage.py makemigrations 
      python src/manage.py migrate
      python src/manage.py collectstatic 
      python src/manage.py runserver 
      ```
