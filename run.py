from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import pymysql.cursors
import json
import sys

app = FlaskAPI(__name__)
CORS(app)

# ----------  DATABASE CREDENTIALS  ----------
USERNAME = 'root'
PASSWORD = 'webdev'
DBNAME   = 'cs3200final'
# --------------------------------------------

PASS = 'success'
FAIL = 'fail'

con = ''


def sendResponse(status, data):
    return {
        'status': status,
        'data': data
    }


def openConnection():
    global con
    try:
        con = pymysql.connect(host='localhost',
                      user=USERNAME,
                      password=PASSWORD,
                      db=DBNAME,
                      charset='UTF8MB4',
                      cursorclass=pymysql.cursors.DictCursor)

    except:
        print('Could not establish database connection.', file=sys.stderr)
        print('Make sure login credentials in run.py are correct.', file=sys.stderr)


@app.route('/reviews', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'GET':
        with con.cursor() as cursor:
            sql = "SELECT * FROM reviews;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return sendResponse(PASS, result)

    elif request.method == 'POST':
        try:
            with con.cursor() as  cursor:
                sql = "INSERT INTO reviews (movie_id, reviewer_id, rating, description) VALUES ("
                sql = sql + str(request.data["movie_id"]) + ", "
                sql = sql + str(request.data["reviewer_id"]) + ", "
                sql = sql + str(request.data["rating"]) + ", '"
                sql = sql + request.data["description"] + "');"
                cursor.execute(sql)
                return sendResponse(PASS, "")
        except:
            return sendResponse(FAIL, 'BAD INPUTS')

openConnection()
