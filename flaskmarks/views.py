from flask import (
    render_template,
    flash,
    redirect,
    session,
    url_for,
    g,
    request,
    )

from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
    login_required,
    )

from flaskmarks import app

from forms import (
    LoginForm,
    )

from models import (
    User,
    Bookmark,
    )

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html',
          title = 'Home')

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()
    if form.validate_on_submit():
        u = User.by_username(form.username.data)
        if u and u.authenticate_user(form.password.data):
            flash('Successful login request for %s' % (form.username.data))
            #login_user(u)
        else:
            flash('Failed login request for %s' % (form.username.data))
        return redirect('/index')
    return render_template('login.html',
            title = 'Login',
            form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
