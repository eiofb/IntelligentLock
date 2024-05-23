from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
import string, random
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return jsonify({"code": 500, "message": "", "data":
                    {"emailError": "邮箱在数据库不存在！"}})
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                return jsonify({"code": 200, "message": "", "data": None})
            else:
                return jsonify({"code": 500, "message": "", "data":
                    {"passwordError": "密码错误！"}})
        else:
            return jsonify({"code": 500, "message": "", "data": form.errors})

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits * 4
    captcha = "".join(random.sample(source, 4))
    message = Message(subject="captcha", recipients=[email], body=f"captcha:{captcha}")
    mail.send(message)

    email_captcha = EmailCaptchaModel.query.filter_by(email=email).first()
    if email_captcha:
        email_captcha.captcha = captcha
    else:
        email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)

    db.session.commit()
    return jsonify({"code": 200, "message": "", "data": None})

@bp.route("/mail/test")
def mail_test():
    message = Message(subject="mail_test", recipients=["e719304290@outlook.com"], body="This is a test message!")
    mail.send(message)
    return "send success!"

@bp.route("logout")
def logout():
    session.clear()
    return redirect("/")