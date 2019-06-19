from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import pymysql.cursors

app = FlaskAPI(__name__)


# ----------  DATABASE CREDENTIALS  ----------
USERNAME = 'root'
PASSWORD = 'webdev'
DBNAME   = 'cs3200final'
# --------------------------------------------


con = ''


def openConnection():
    global con
    try:
        con = pymysql.connect(host='localhost',
                      user=USERNAME,
                      password=PASSWORD,
                      db=DBNAME,
                      charset='UTF8MB4',
                      cursorclass=pymysql.cursors.DictCursor)
        with con.cursor() as cursor:
            sql = "SELECT * FROM movies;"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    except:
        print('Could not establish database connection.')
        print('Make sure login credentials in run.py are correct.')
        raise
        


@app.route('/movies', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'GET':
        return movies
    elif request.method == 'POST':
        movies.add({'title': "garfield's day off",
                    'director': 'Edward Snowden'})


openConnection()
