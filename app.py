from flask import Flask, session, g
from flask_redis import FlaskRedis
from flask_migrate import Migrate
import config
from extensions import db, mail, cache
import os
from blueprints.user import bp as user_bp
from blueprints.homepage import bp as homepage_bp
from usermodel import UserModel

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# 设置 secret_key，使用 os.urandom(24) 生成随机密钥
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

db.init_app(app)
mail.init_app(app)

# Redis 連接配置
app.config['REDIS_URL'] = "redis://localhost:6379/0"
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = app.config['REDIS_URL']
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache.init_app(app)
# 设置上传文件夹
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
# 可选：限制上传文件的大小
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

migrate = Migrate(app, db)
app.register_blueprint(user_bp)
app.register_blueprint(homepage_bp)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.filter((UserModel.email == user_id) | (UserModel.username == user_id)).first()
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='80')