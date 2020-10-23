from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from qaf import db
from qaf.models import Question, User
from qaf.forms.forms import QuestionForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    questions = Question.query.all()
    return render_template('home.html', questions=questions)


@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.data.get('question')
        expert = form.data.get('expert')
        expert = User.query.filter_by(id=int(expert)).first()

        question = Question(
            question=question,
            expert_id=expert.id,
            asked_by_id=current_user.id
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.home'))

    experts = User.query.all()
    context = {
        'experts' : experts,
        'form' : form
    }
    return render_template('ask.html', **context)


@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    if not current_user.expert:
        return redirect(url_for('main.home'))

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('main.unanswered'))
    context = {
        'question' : question
    }
    return render_template('answer.html', **context)


@main.route('/question/<int:question_id>')
def question(question_id):
    question = Question.query.get_or_404(question_id)
    context = {
        'question' : question
    }
    return render_template('question.html', **context)


@main.route('/unanswered')
@login_required
def unanswered():
    if not current_user.expert:
        return redirect(url_for('main.home'))

    unanswered_questions = Question.query\
        .filter_by(expert_id=current_user.id)\
        .filter(Question.answer == None)\
        .all()
    context = {
        'unanswered_questions' : unanswered_questions
    }
    return render_template('unanswered.html', **context)


@main.route('/promote/<int:user_id>')
@login_required
def promote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.home'))
    user = User.query.get_or_404(user_id)
    user.expert = True
    db.session.commit()
    return redirect(url_for('main.users'))