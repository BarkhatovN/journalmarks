from flask import Flask, render_template, url_for
from app import app
from app.static.get_marks import get_user_subject_marks
from app.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login, password = form.login.data, form.password.data
        try:
            user, subject_marks = get_user_subject_marks(login, password)
            subjects = sorted(subject_marks.keys())
            return render_template(
                'output.html',
                user=user,
                subjects=subjects,
                subject_marks=subject_marks)
        except Exception as exc:
            return exc.args

    return render_template('login.html', title='Sign In', form=form)
