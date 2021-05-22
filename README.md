# Pre-requisites

1. Python 3.8
2. Postgres

# Setup Guide

1. Clone the repository
2. Create a virtual environment
   ```
   python -m venv env
   ```
3. Activate the virtual environment

   Windows:

   ```
   env\Scripts\activate.bat
   ```

   UNIX:

   ```
   source env/bin/activate
   ```

4. Install requirements

   ```
   pip install -r requirements.txt
   ```

5. Create a new postgres database.
6. Create a new file named `.env` and copy the contents of `.env.example` in it. Then fill in all the relevant variables like the `DATABASE_URL` etc..
7. Migrate the database and run the project

   ```
   python manage.py migrate
   python manage.py runserver
   ```

   MAKE SURE that the python you are using is being sourced from the environment that you created. Else you might face an error like this:

   ```python
   RuntimeError: populate() isn't reentrant
   ```

8. If everything goes well, you can access the development server on
   ```
   http://localhost:8000/
   ```
