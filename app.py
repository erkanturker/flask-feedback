from flask import Flask,redirect,request,render_template,flash,session,abort
from models import connect_db,db,User,Feedback
from forms import RegisterUserForm,UserLoginForm,FeedbackForm
from werkzeug.exceptions import Unauthorized

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
    if "username" in session:
        redirect(f"users/{session['username']}")
    else:    
     return redirect("/register")

@app.route("/register", methods=['GET','POST'])
def register_user():
    """Register User"""

    session_username = session.get("username",None)

    if session_username:
        return redirect(f"/users/{session_username}")

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
        session['username']= new_user.username
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("register_form.html", form = form)

@app.route("/login",methods=['GET','POST'])
def login_user():
    """Produce login form or handle login."""
    session_username = session.get("username",None)

    if session_username:
        return redirect(f"/users/{session_username}")


    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate_user(username=username,password=password)
        if user:
            session['username']= user.username
            flash("You logged in", "success")
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors=['Bad Username/Password']
            flash("Login Failed", "danger")

    return render_template("login.html",form=form)
    
@app.route("/users/<string:username>")
def show_secret(username):
    session_username = session.get("username",None)
    if session_username==username:
        user = User.query.filter_by(username=username).first()
        feedbacks = Feedback.query.all()
        return render_template("user_details.html",user=user,feedbacks=feedbacks)
    else: 
        flash("Only Authorized Users see the content", "danger")
        return redirect("/login")
    
@app.route("/logout")
def logout_user():
    if "username" in session:
        session.pop("username")
        flash("Goodbye!", "info")
    return redirect('/login')

@app.route("/users/<string:username>/feedback/add",methods=['GET','POST'])
def add_feedback(username):
    form = FeedbackForm()

    session_username = session.get("username",None)
    if session_username==username:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title,content=content,username=username)
            db.session.add(feedback)
            db.session.commit()
            flash('Post added successfully', 'success')
            return redirect(f"/users/{username}")
        else:
         return render_template("add_feedback.html",form=form)
        
@app.route("/feedback/<int:feedback_id>/update",methods=['GET','POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.user.username
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Post updated successfully', 'success')
        return redirect(f"/users/{username}")
    else:
        return render_template('update_feedback.html', form=form)


@app.route("/feedback/<int:feedback_id>/delete",methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    username = feedback.user.username
    db.session.delete(feedback)
    db.session.commit()
    flash('Post updated successfully', 'danger')
    return redirect(f"/users/{username}")

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404