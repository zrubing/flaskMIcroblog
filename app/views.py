from app import app,lm,db,oid
from flask import render_template
from .forms import LoginForm
from flask import flash,redirect


@app.route("/")
@app.route("/index")
def index():
    user={'nickname':'haha'}
    posts=[
        {
            'author':{'nickname':'John'},
            'body':'nice day'
        },
        {

            'author':{'nickname':'khan'},
            'body':'good boy'
        }]
    return render_template('index.html',title='home',user=user,posts=posts)

@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash('Login request for openID:'+form.openid.data)
        return redirect('/index')
    return render_template('login.html',title='Sign In',form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

