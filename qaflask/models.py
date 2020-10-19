from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime as dt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from qaflask import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    expert = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    
    questions_asked = db.relationship(
        'Question', 
        foreign_keys='Question.asked_by_id', 
        backref='asker', 
        lazy=True
    )
    
    answer_requested = db.relationship(
        'Question', 
        foreign_keys='Question.expert_id', 
        backref='expert', 
        lazy=True
    )

    def __repr__(self):
        return f"User: {self.username}, Email: {self.email}, Image: {self.image_file}"

    def get_reset_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @property
    def not_hashed_password(self):
        raise AttributeError('Cannot view unhashed password!')

    @not_hashed_password.setter
    def not_hashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)
   
 
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    asked_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Question: {self.question}, {self.answer}, {self.asked_by_id}"
