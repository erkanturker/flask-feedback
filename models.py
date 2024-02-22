from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt =Bcrypt()

def connect_db(app):
    """Connect DB"""
    db.app = app
    db.init_app(app)
    bcrypt.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register_user(cls,username,password,email,first_name,last_name):
         """Register user w/hashed password & return user."""

         hashed = bcrypt.generate_password_hash(password)
         hashed_utf = hashed.decode("utf8")
         
         return cls(username=username,password=hashed_utf,email=email,first_name=first_name,last_name=last_name)
    
    @classmethod
    def authenticate_user(cls,username,password):
        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


    def __repr__(self):
        return f"<User: username={self.username} password={self.password} email={self.email} first_name={self.first_name} last_name={self.last_name}>"

class Feedback(db.Model):
    __tablename__="feedbacks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username= db.Column(db.String, db.ForeignKey("users.username"), nullable=False) 

    user = db.relationship("User",backref="feedbacks")

