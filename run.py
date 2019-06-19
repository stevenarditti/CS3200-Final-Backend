from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import pymysql.cursors

app = FlaskAPI(__name__)


# ----------  DATABASE CREDENTIALS  ----------
USERNAME = 'root'
PASSWORD = '3200final'
DBNAME   = '3200finaldb'
# --------------------------------------------

movies = [{'title': 'lotr','director': 'Spencer'},
          {'title': 'cars 2','director': 'Steve'}]

##con = pymysql.connect(host='localhost',
##                      user=USERNAME,
##                      password=PASSWORD,
##                      db=DBNAME,
##                      charset='UTF8MB4',
##                      cursorclass=pymysql.cursors.DictCursor)


@app.route('/movies', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'GET':
        return movies
    elif request.method == 'POST':
        movies.add({'title': "garfield's day oof",
                    'director': 'Edward Snowden'})
