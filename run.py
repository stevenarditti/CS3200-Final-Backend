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
        print('Could not establish database connection.')


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
                con.commit()
                return sendResponse(PASS, "")
        except Exception as e:
            return sendResponse(FAIL, 'BAD INPUTS')


@app.route('/reviews/<int:id>', methods=['GET', 'PUT'])
def get(id):
  if request.method == 'GET':
    sql = "SELECT * FROM reviews WHERE review_id = {};".format(id)
    try:
        with con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return sendResponse(PASS, result)
    except Exception as e:
        return sendResponse(FAIL, e)
  else:
    try:
      body = request.data
      with con.cursor() as  cursor:
        sql = "UPDATE reviews set movie_id = {}, reviewer_id = {}, rating = {}, description = '{}' WHERE review_id = {};".format(body['movie_id'], body['reviewer_id'], body['rating'], body['description'], body['review_id'])
        cursor.execute(sql)
        con.commit()
        return sendResponse(PASS, "")
    except Exception as e:
      print e
      return sendResponse(FAIL, 'BAD INPUTS')


@app.route('/reviews/delete/<int:id>', methods=['DELETE'])
def delete(id):
    sql = "DELETE FROM reviews WHERE review_id = {};".format(id)
    try:
        with con.cursor() as cursor:
            cursor.execute(sql)
            con.commit()
            sql = "SELECT * FROM reviews;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return sendResponse(PASS, result)
    except Exception as e:
        return sendResponse(FAIL, e)


@app.route('/dropdown')
def dropdown():
  sql = "SELECT movie_id, title from movies;"
  try: 
    with con.cursor() as cursor:
      cursor.execute(sql)
      movies = cursor.fetchall()
      sql = "SELECT reviewer_id, name from reviewers;"
      cursor.execute(sql)
      reviewers = cursor.fetchall()
      return sendResponse(PASS, {"reviewers": reviewers, "movies": movies})
  except Exception as e:
    return sendResponse(FAIL, e)

openConnection()
