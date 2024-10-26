from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = "forumuser"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # 增加长度并更改字段名
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # 存储哈希值

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # 校验密码哈希值

class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(300), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey("forumuser.id"))
    author = db.relationship(UserModel, backref="posts")
    
    vote_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Post {self.title}>"

class CommentModel(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    post_id = db.Column(db.Integer, db.ForeignKey("post_model.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("forumuser.id"))

    question = db.relationship(PostModel, backref=db.backref("comments", order_by=create_time.desc()))
    user = db.relationship(UserModel, backref="comments")
