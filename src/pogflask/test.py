import os, sys, re

from flask import Flask
from flask import request
from flask import current_app
from flask import render_template
from flask import session, redirect, url_for, flash

from flask_script import Shell

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

from flask_wtf import Form

from wtforms            import StringField, SubmitField
from wtforms.validators import Required

from flask_script       import Manager
from flask_bootstrap    import Bootstrap

app       = Flask(__name__)

app.config['SECRET_KEY']                    = 'the owl and the pussycat'

app.config['SQLALCHEMY_DATABASE_URI']       = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

manager   = Manager(app)
bootstrap = Bootstrap(app)

# =====================================================================================
#
# Shell integration stuff
#
# =====================================================================================


def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))


# =====================================================================================
# Database stuff

class Role(db.Model):
    
    __tablename__ = 'roles'
    
    id   = db.Column(db.Integer,    primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role')                  #  
    
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):

    __tablename__ = 'users'

    id        = db.Column(db.Integer,   primary_key=True)
    username  = db.Column(db.String(64), unique=True,  index=True)

    role_id   = db.Column(db.Integer,  db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username



# from test import db
# db.create_all()

# from test import Role, User

# admin_role = Role(name='Admin')
# mod_role  = Role(name='Moderator')
# user_role = Role(name='User')

# user_john = User(username='john',role=admin_role)
# user_susan = User(username='susan',role=user_role)
# user_david = User(username='david',role=user_role)
#>>> db.session.add(admin_role)
#>>> db.session.add(mod_role)
#>>> db.session.add(user_role)
#>>> db.session.add(user_john)
#>>> db.session.add(user_susan)
#>>> db.session.add(user_david)
#>>> db.session.commit()
#>>> print (admin_role.id)
#1

@app.route('/', methods=['GET','POST'])
def index():
    #user_agent = request.headers.get('User-Agent')

    #str = '<p>Your browser is %s</p>' % user_agent
    #str = str +  '<p>Your current app is %s</p>' % current_app.name

    #for map in app.url_map:
    #    str = str + map
        
    #return str
#   return '<h1>Hello Pog!</h1>'

    name = None
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')

        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name")

        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True

        
        session['name'] = form.name.data                  # Saves the name in a session variable so a reload works.
        form.name.data = ''
        
        return redirect(url_for('index'))
    
    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known'))

#    return render_template('derived.html')

@app.route('/user/<name>')
def user(name):
    #return '<h1>Hello, %s</h1>' % name
    form = NameForm()
    
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        
    return render_template('user.html',form=form,name=name)

@app.before_request
def before_first_request():
    str = "This is before the first request"


class NameForm(Form):
    name   = StringField('What is your name?',validators=[Required()])
    submit = SubmitField('Submit')




# =====================================================================================
# Templates - variables

# Templates can recognise various types of data structure e.g

#< p > A value from a dictionary: {{ mydict[' key'] }}.</ p >
#< p > A value from a list: {{ mylist[ 3] }}. </ p >
#< p > A value from a list, with a variable index: {{ mylist[ myintvar] }}. </ p >
#< p > A value from an object's method: {{ myobj.somemethod() }}. </ p >


# Variables can be modified with filters e.g. {{ name|capitalize }}

# Also safe/lower/upper/title/trim/striptags

# Templates - control structures

#{% if user %}
#    Hello, {{ user }}!
#{% else %}
#    Hello, stranger
#{% endif %}


# Rendering a list

#<ul>
#   {% for comment in comments %}
#       <li>{{ comment }}</li>
#   {% endfor %}
#</ul>

# Also macros (like functions

# {% macro render_comment(comment) %}
#   <li>{{ comment }}</li>
# {% endmacro %}

#<ul>
#   {% for comment in comments %}
#       {{ macros.render_comment(comment) }}
#   {% endfor %}
#</ul>

# Templates - control structures

#{% if user %}
#    Hello, {{ user }}!
#{% else %}
#    Hello, stranger
#{% endif %}


# Rendering a list

#<ul>
#   {% for comment in comments %}
#       <li>{{ comment }}</li>
#   {% endfor %}
#</ul>

# Also macros (like functions

# {% macro render_comment(comment) %}
#   <li>{{ comment }}</li>
# {% endmacro %}

#<ul>
#   {% for comment in comments %}
#       {{ macros.render_comment(comment) }}
#   {% endfor %}
#</ul>


# Importing code

# {% import 'macros.html' as macros %}
# {% for comment in comments %}
#      {{ macros.render_comment(comment }}
# {% endfor %}


# Bootstrap blocks

#{% extends "bootstrap/base.html" %}

#{% block title %}Flasky{% endblock %}
#{% block navbar %}
#<div class="navbar navbar-inverse" role="navigation">
#  <div class="container">
#    <div class="navbar-header">
#      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">#
#	<span class="sr-ony">Toggle navigation</span>
#	<span class="icon-bar"></span>
#	<span class="icon-bar"></span>
#	<span class="icon-bar"></span>
 #     </button>
#      <a class="navbar-brand" href="/">Flasky</a>
#    </div>
#    <div class="navbar-collapse collapse">
#      <ul class="nav navbar-nav">#
#	<li><a href="/">Home</a></li>
#      </ul>
#    </div>
#  </div>
#</div>
#{% endblock %}

#{% block content %}
#   <div class="container">
#     <div class="page-header">
#       <h1>Hello, {{ name }}!</h1>
#     </div>
#     </div>
#{% endblock %}


# Other blocks

# doc    The entire html doc
# html_attribs     attributes inside the <html> tag
# html             contents of the html tag
# head             contents of the head tag
# title            contents of the title tag
# metas            list of <meta> tags 
# styles           css defuinitions
# body_attribs     attributes inside the body tag
# navbar            user-defined navigation bar
# content          user-defined page content
# scripts          javascript declarations at the bottom of the documenbt

# Many are used by bootstrap itself so : 
#{% block scripts %}
#  {{ super() }}
#  < script type =" text/ javascript" src =" my-script.js" > </ script >
#{% endblock %}

# Links


# url_for('user',name='pog',_external=True)

if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
