from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,TextAreaField,PasswordField,validators,SubmitField, TextField
from passlib.hash import sha256_crypt
from functools import wraps
app=Flask(__name__)
#config MySQLapp
app.secret_key='i_am_very_goodgirl'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Sunny#2002@@localhost/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)
class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    email=db.Column(db.String(100))
    username=db.Column(db.String(30))
    password=db.Column(db.String(200))
    registered_date=db.Column(db.DateTime)
    article_key=db.relationship('Articles', backref='users', lazy=True)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.String(10000))
    user_key = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

class RegisterForm(Form):
    name=TextField('name')
    email=TextField('email')
    username=TextField('username')
    password=PasswordField('password')
    confirm=PasswordField('confirm password')
    submit=SubmitField("Create new user")

class ArticleForm(Form):
    title=TextField('Title',[validators.Length(min=1,max=200)])
    body=TextField('Body',[validators.Length(min=30)])


class LoginForm(Form):
    username=TextField('username')
    password=PasswordField('password')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if request.method=='POST':
        form=request.form
        name=form['name']
        email=form['email']
        username=form['username']
        password=form['password']
        #create cursor
        insert_data = Users(name = name, email = email, username = username, password = password)
        save_to_database = db.session
        try:
            save_to_database.add(insert_data)
            save_to_database.commit()
            return "added successfully"
        except:
            save_to_database.rollback()
            save_to_database.flush()
            return 'im in except'
    return render_template('register.html',form=form)
    # else:
    #     return render_template('register.html',form=form,msg=msg)

@app.route('/login/',methods=['GET','POST'])
def login():
    # print('im sravya')
    # form=LoginForm()
    # form=request.form
    #
    # user = Users.query.filter_by(username=form['username']).first()
    # if sha256_crypt.verify(form['username'],user.password):
    #     print(user.password)
    #     msg="loggeed in"
    #     return redirect(url_for('dashboard'))
    # return render_template('login.html',form=form)
     user=''
     if request.method=='POST':
         form=LoginForm(request.form)

         username=request.form['username']
         print(username)
         password=request.form['password']
         print(password)
        # data=Users.session.fetchOne()
        # password=data['password']
        # print('password is ',password)
        #     #compare passwords
        # if sha256_crypt.verify(password_candidate,password):
        #
        #     session['logged_in']=True
        #     session['username']=username
        #     flash('you are now logged in','success')
        #     return redirect(url_for('dashboard'))
        # else:
        #     error='Invalid login'
        #     return render_template('login.html',error=error)
         user = Users.query.filter_by(username=username).first()
         print(user.username)
         print(user.password)
         try:
             if password==user.password:

                 return render_template('dashboard.html')
             else:
                 flash('please check again')
         except:
             return 'usesrname not found'
         return render_template('login.html')
     # if password is not user.password:
     #     flash('Please check your login details and try again')
     #     return render_template('login.html')
     # else:
     #     return redirect(url_for('dashboard'))

    # else:
    #     error='usesrname not found'
    #     return render_template('login.html',error=error)

     return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('unauthorised,please login','danger')
            return redirect(url_for('login'))
    return wrap
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html',msg=msg)

if __name__=="__main__":
    db.create_all()
    app.run(debug=True, port = 8000)
