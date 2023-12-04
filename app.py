"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'm@rryAchie'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    '''homepage redirects to list of users'''

    return redirect('/users')

# User route


@app.route('/users')
def users_index():
    '''provide info to list of users'''

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    '''Create new user form'''

    return render_template('users/new.html')


@app.route('/users/new', methods=['POST'])
def users_new():
    '''handle new user submission'''

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def users_show(user_id):
    '''user profile page'''

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    '''page for user to edit info'''

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    '''update user profile upond submission'''

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


if __name__ == '__main__':
    with app.app_context().push():
        app.run(debug=True)
