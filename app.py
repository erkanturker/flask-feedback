from flask import Flask,redirect,request,render_template,flash,session
from models import connect_db,db,User
from forms import RegisterUserForm,UserLoginForm

app= Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


with app.app_context():
    connect_db(app)
    db.create_all()

@app.route("/")
def show_root():
    return redirect("/register")

@app.route("/register", methods=['GET','POST'])
def register_user():
    """Register User"""

    form =RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email= form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        flash(f"User is created","success")
        return redirect("/secret")
    else:
        return render_template("register_form.html", form = form)

@app.route("/login",methods=['GET','POST'])
def login_user():
    """Produce login form or handle login."""

    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate_user(username=username,password=password)
        if user:
            session['username']= user.username
            flash("You logged in", "success")
            return redirect("/secret")
        else:
            form.username.errors=['Bad Username/Password']
            flash("Login Failed", "danger")

    return render_template("login.html",form=form)
    
@app.route("/secret")
def show_secret():
    username = session.get("username",None)
    if username:
        return render_template("secret.html")
    else: 
        flash("Only Authorized Users see the content", "danger")
        return redirect("/login")