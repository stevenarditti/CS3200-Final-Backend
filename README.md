CS3200DB

Flask server running on localhost:5000
Acts as an API only, must be run alongside React front end.

ASSUMES CREDITIALS:
username: root
password: webdev
database: cs3200final
If other credentials are used, configure the global variables in run.py
to reflect proper login credentials.

To run:

1. Create new directory
2. In that directory, run “git clone https://github.com/stevenarditti/CS3200-Final-Backend”
3. Run the MySQL data dump (database_dump.sql)in MySQLWorkbench to set up the schemas and load the DB. 
4. in run.py on line 13, change password to your MySQLWorkbench root password. 
5. run “pip install flask flask_api flask_cors pymysql”
6. If on Mac, type “export FLASK_APP=run.py” followed by “python -m flask run”
7. If on Windows, set FLASK_APP=run.py python -m flask run

