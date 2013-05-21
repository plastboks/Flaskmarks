from flask import (
  render_template,
  flash,
  redirect,
  )
from flaskmarks import app
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html',
          title = 'Home')

@app.route('/login', methods=['GET', 'POST'])
def login(): 
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for Username="' + form.username.data)
    return redirect('/index')
  return render_template('login.html',
          title = 'Login',
          form = form)
