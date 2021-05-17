# Pre-requisites

1. Python 3.9
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

   On Windows, `mysqlclient` installation might fail. In that case, visit [this website](https://www.lfd.uci.edu/~gohlke/pythonlibs/) and download the `mysqlclient` that is compatible with your python version.

   Here's how to find the correct file:

   - cp38 means for Python 3.8 and cp37 means for Python 3.7 and so on... So, first check your python version whether it is 3.8, 3.7, 3.6, 3.5, 3.4 then download accordingly.

   - While checking python version also check whether your python is 64-bit or 32-bit (It shows up right next to the version). If your python is 32-bit then select amd32. If it's 64-bit then select amd64.

   Install it using

   ```
   pip install <path-to-downloaded-file>
   ```

   After this, you will need to remove the `mysqlclient==1.4.6` written in the `requirements.txt` file. Then install the requirements again using the first command, then if everything goes well, undo the changes that you made in the `requirements.txt` file.

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
