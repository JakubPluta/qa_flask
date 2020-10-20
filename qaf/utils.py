import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from qaf import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile', picture_fn)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)

    img.save(picture_path)
    return picture_fn


def send_reset_token(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])

    msg.body = f"""To reset your password, please visit the following link:
    {url_for('users.reset_password',token=token, _external=True)}

    If you did not make this request then simple ignore this email and no change it!
    """

    mail.send(msg)