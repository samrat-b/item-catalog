from dbsetup import Level, Base, Course
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, request, redirect, render_template, url_for

from flask import session as login_session
import string
import random

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Learn German App"


engine = create_engine('sqlite:///germancourse.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

# Signin functionality
# @app.route('/login/')
# def signIn():
#     state = ''.join(random.choice(string.ascii_uppercase + string.digits)
#                     for x in xrange(32))

#     login_session['state'] = state
#     return render_template('home.html', STATE=state)
# List down all German Course Levels
@app.route('/')
# @app.route('/level/')
@app.route('/home/')
def listLevels():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))

    login_session['state'] = state
    levels = session.query(Level).all()
    # return "All levels"
    return render_template('home.html', levels=levels, STATE=state)
    # return render_template('home.html', levels=levels)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    levels = session.query(Level).all()
    # return "All levels"
    return render_template('home.html', levels=levels)


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# List down Courses of a particular level
@app.route('/level/<int:level_id>')
def listCourses(level_id):
    # return "Courses"
    levelCourses = session.query(Course).filter_by(level_id=level_id).all()
    levelName = session.query(Level).filter_by(id=level_id).one().name
    # return redirect('levelCourses', levelCourses=levelCourses, levelName=levelName)
    return render_template('levelCourses.html', levelCourses=levelCourses, levelName=levelName)

# Add a new Course to a level
# @app.route('/level/<int:level_id>/course/add', methods=['GET', 'POST'])
@app.route('/course/add', methods=['GET', 'POST'])
def newCourse():
    if request.method != 'GET':
        # return "Redirect to levelCourses Page"
        addCourse = Course(name=request.form['course'], details=request.form['detail'],
                           level_id=session.query(Level).filter_by(name=request.form['level']).one().id)
        session.add(addCourse)
        session.commit()
        level_id = session.query(Level).filter_by(
            name=request.form['level']).one().id
        return redirect(url_for('listCourses', level_id=level_id))
    else:
        levels = session.query(Level).all()
        return render_template('newCourse.html', levels=levels)


# Edit a Course of a level
@app.route('/level/<int:level_id>/course/<int:course_id>/modify', methods=['GET', 'POST'])
def editCourse(level_id, course_id):
    if request.method != 'GET':
        modifiedCourse = session.query(Course).filter_by(id=course_id).one()
        if request.form['course']:
            modifiedCourse.name = request.form['course']
        if request.form['detail']:
            modifiedCourse.details = request.form['detail']
        session.add(modifiedCourse)
        session.commit()
        return redirect(url_for('listCourses', level_id=level_id))
    else:
        course = session.query(Course).filter_by(id=course_id).one()
        return render_template('editCourse.html', course=course)

# Delete a Course of a level
@app.route('/level/<int:level_id>/course/<int:course_id>/remove', methods=['GET', 'POST'])
def delCourse(level_id, course_id):
    removeSelCourse = session.query(Course).filter_by(id=course_id).one()
    if request.method != 'GET':
        session.delete(removeSelCourse)
        session.commit()
        return redirect(url_for('listCourses', level_id=level_id))
    else:
        return render_template('delCourse.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)