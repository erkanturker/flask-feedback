from flask import Flask,redirect,request,render_template,flash
from models import connect_db,db,User
from forms import RegisterUserForm

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
        flash(f"User is created")
        return redirect("/secret")
    else:
        return render_template("register_form.html", form = form)
    
@app.route("/secret")
def show_secret():
    return render_template("secret.html")