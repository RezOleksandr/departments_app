# EPAM Online Python External Course - Department Management App

## About application

This is simple web application for managing departments and employees. With this app user can: 
* view a list of all departments;
* view a list of employees and apply filters to it;
* create new departments and employees, edit their data or delete them.

## How to build

To run this app you need to have Python 3.9 or newer installed. This instruction describes how to build this app on Ubuntu Linux machines.

1. Open a command line interface
2. Clone this GitHub repository and open the project directory

       git clone https://github.com/RezOleksandr/epam_python_project
       cd epam_python_project/

3. Create a virtual environment and activate it

        python -m venv venv
        source venv/bin/activate

4. Install the app

        python setup.py install

5. Install PostgreSQL, and create a database

    - Install PostgreSQL

          sudo apt install postgresql postgresql-contrib

    - Create a user:

          sudo -u postgres createuser --interactive

    - Create a database:

          sudo -u postgres psql -c 'create database your_database;'
          sudo -u postgres psql -c 'grant all privileges on database your_database to your_user;'

6. Create an instance directory and open it

        mkdir instance
        cd instance/

7. Create a configuration file

    - Create and open a file using nano

          nano config.py

    - Create a database connection uri variable

          SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://your_user:your_user_password@localhost:5432/your_database'

    - Press Ctrl + C to close the file, then press Y to confirm saving changes, than press Enter to confirm

8. Return to the project directory and start the app

        cd ..
        python wsgi.py

The app should be available on http://localhost:5000/departments