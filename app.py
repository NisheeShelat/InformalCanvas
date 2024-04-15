from flask import Flask, render_template, url_for, request, redirect, session
from server.fse_firebase import Firebase
import pyrebase

app = Flask(__name__)
app.secret_key = "notasecretkey"
firebaseConfig = {
    # 'apiKey': "",
    'authDomain': "codecrushers-83ba1.firebaseapp.com",
    'databaseURL': "https://codecrushers-83ba1-default-rtdb.firebaseio.com",
    # 'projectId': "",
    # 'storageBucket': "",
    # 'messagingSenderId': "",
    # 'appId': "",
    # 'measurementId': ""
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

firebaseData = Firebase()
firebaseData.initialize()


@app.route('/', methods=['POST', 'GET'])
def home():
    # Always render home template
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            # if firebase.login_user(email, password):
            #     session['user'] = email
            # else:
            #     assert False, "Could not log in, incorrect password."
            return render_template('home.html')
        except Exception as e:
            print(e)
            return '<a href="/login">There was a problem with logging in, or the user was ' \
                   'not a valid user. Return to login.</a>'

    return render_template('login.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            print("Got email:" + email)
            password = request.form.get('password')
            print("Got password:" + password)
            new_user = auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            return render_template('home.html')
        except Exception as e:
            return render_template('signup.html', )
            print(e)
            return '<a href="/signup">There was a problem with signing up. Return to signup.</a>'

    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session['user']:
        user_removed = session.pop('user')
        print("Logged out user: " + user_removed)

    return render_template('home.html')


@app.route('/browse', methods=['GET'])
def browse():
    # Request data from firebase, get list of dictionaries
    course_list = firebaseData.get_course_list(9)
    return render_template('browse.html', data=course_list)


@app.route('/course-<course_id>', methods=['GET'])
def course(course_id):
    # course_id is course_name (hyphenated) + index
    course_json = firebaseData.get_by_course_id(course_id)
    return render_template('course.html', data=course_json)


if __name__ == '__main__':
    app.run(debug=True)
