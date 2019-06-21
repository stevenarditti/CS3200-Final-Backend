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
def get_reviews():
    if request.method == 'GET':
        with con.cursor() as cursor:
            sql = "SELECT * FROM reviews r "
            sql += "JOIN movies m ON r.movie_id = m.movie_id "
            sql += "JOIN reviewers re ON r.reviewer_id = re.reviewer_id;"
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
        except:
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
    except:
        return sendResponse(FAIL, '')
  else:
    try:
      body = request.data
      with con.cursor() as  cursor:
        sql = "UPDATE reviews set movie_id = {}, reviewer_id = {}, rating = {}, description = '{}' WHERE review_id = {};".format(body['movie_id'], body['reviewer_id'], body['rating'], body['description'], body['review_id'])
        cursor.execute(sql)
        con.commit()
        return sendResponse(PASS, "")
    except:
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
    except:
        return sendResponse(FAIL, '')


@app.route('/movies/<int:id>/', methods=['GET'])
def get_movies(id):
    sql = "SELECT * FROM movies WHERE movie_id = {};".format(id)
    try:
        with con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return sendResponse(PASS, result)
    except:
        return sendResponse(FAIL, '')


@app.route('/movies/<int:id>/actors/', methods=['GET'])
def get_movie_actors(id):
    try:
        with con.cursor() as cursor:
            sql = "SELECT name, biography, headshot_url FROM cast_members c "
            sql += "JOIN movies m ON c.movie_id=m.movie_id "
            sql += "JOIN actors a ON c.actor_id=a.actor_id "
            sql += "WHERE c.movie_id = {};".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return sendResponse(PASS, result)
    except:
        sendResponse(FAIL, '')



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
