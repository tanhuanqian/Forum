import wtforms
from wtforms.validators import Email, Length, EqualTo, DataRequired
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from usermodel import UserModel

class RegisterForm(wtforms.Form):
    email = StringField('Email', validators=[
        Email(message="Email invalid!"), 
        DataRequired(message="Email is required!")
    ])
    
    username = StringField('Username', validators=[
        Length(min=6, max=20, message="Username must be between 6 and 20 characters long!"), 
        DataRequired(message="Username is required!")
    ])
    
    password = PasswordField('Password', validators=[
        Length(min=6, max=20, message="Password must be between 6 and 20 characters long!"), 
        DataRequired(message="Password is required!")
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        EqualTo('password', message="Passwords must match!"), 
        DataRequired(message="Please confirm your password!")
    ])

    code = StringField('Verification Code', validators=[DataRequired(message="Verification code is required!")])
    
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError("Email address has been taken.")
        
    def validate_username(self, field):
        username = field.data
        user = UserModel.query.filter_by(username=username).first()
        if user:
            raise wtforms.ValidationError("Username has been taken.")

class LoginForm(wtforms.Form):
    account_type = wtforms.SelectField(choices=[('email', 'Email'), ('username', 'Username')], validators=[DataRequired()])
    account = wtforms.StringField(validators=[DataRequired()])
    password = wtforms.StringField(validators=[DataRequired()])

    def validate_account(self, field):
        """验证邮箱或用户名是否存在"""
        account = field.data
        account_type = self.account_type.data
        self.user = None  # 用于保存用户对象
        
        if account_type == 'email':
            self.user = UserModel.query.filter_by(email=account).first()
            if not self.user:
                raise wtforms.ValidationError("Email not found")
        else:
            self.user = UserModel.query.filter_by(username=account).first()
            if not self.user:
                raise wtforms.ValidationError("Username not found")

    def validate_password(self, field):
        """验证密码是否正确"""
        password = field.data
        if self.user and not self.user.check_password(password):
            raise wtforms.ValidationError("Password is wrong")

class ContentForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message="Betwwen 3 and 100 words")])
    content = wtforms.StringField(validators=[Length(min=3,message="At least 3 words")])
    image = FileField(validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "Only images are allowed")  # 限制文件类型，但不强制上传
    ])