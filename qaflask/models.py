from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

#todo add email to model


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(150))
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
    
