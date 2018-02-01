"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route('/users')
def user_list():
    """SHow list of users."""

    users = User.query.all()

    return render_template('user_list.html', users=users)


@app.route('/register', methods=['POST'])
def register():
    """Add new user to Users database."""

    input_email = request.form.get('email')
    password = request.form.get('password')

    if db.session.query(User.email).filter(User.email == input_email).all():
        return redirect('/users')
        # redirect to user login page (maybe with flash message)
    else:
        user = User(email=input_email,
                    password=password)

        db.session.add(user)
        db.session.commit()

        return redirect('/')


@app.route('/login')
def log_in():
    """Show the user the login form."""

    return render_template('log_in.html')


@app.route('/login_user', methods=['POST'])
def log_in_user():
    """Handle login form."""

    input_email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == input_email).one()
    if user.password == password:
        session['user_id'] = user.user_id
        flash('You were successfully logged in!')
        return redirect('/')

    else:
        flash('Incorrect password! Please try again.')
        return redirect('/login')


@app.route('/logout')
def logout():
    """Log user out of account."""

    del session['user_id']

    return 'You have successfully logged out.'


#create a login route to show the login page and create a route to handle the login form
# create a session so we can tell if a user is logged in
# flash messages for login and logout

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

