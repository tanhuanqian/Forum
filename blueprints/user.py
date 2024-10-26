from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from extensions import mail, cache, db
from flask_mail import Message
from usermodel import UserModel
from .forms import RegisterForm, LoginForm
import random
import string

bp = Blueprint("user", __name__, url_prefix="/user")

# 用于存储验证码
verification_codes = {}

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            code = form.code.data

            # 从缓存中获取验证码
            cached_code = cache.get(email)
            if cached_code and cached_code == code:
                # 验证码正确，注册用户
                user = UserModel(username=username, email=email)
                user.set_password(password)  # 设置哈希密码
                db.session.add(user)
                db.session.commit()
                flash("Registration successful!", "success")
                return redirect(url_for("homepage.home"))
            else:
                flash("Invalid or expired verification code!", "danger")
        else:
            # 表单验证失败，显示错误
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error, "danger")
    # GET 请求或表单验证失败时渲染注册页面
    return render_template("register.html", form=form)

@bp.route("/send_code", methods=["POST"])
def send_code():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required."}), 400

    # 生成随机验证码
    code = ''.join(random.choices(string.digits, k=4))

    # 发送验证码邮件
    message = Message(subject="Your Verification Code",
                      recipients=[email],
                      body=f"Your verification code is: {code}")
    try:
        mail.send(message)
        cache.set(email, code, timeout=300)
        return jsonify({"message": "Verification code sent!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate(): 
            session['user_id'] = form.account.data
            return redirect(url_for("homepage.home"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(error,"danger")
    return render_template("login.html", form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')