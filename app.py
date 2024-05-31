from flask import Flask, session, g, send_from_directory
import config, os
from exts import db, mail
from blueprints.auth import bp as auth_bp
from blueprints.device import bp as device_bp
from blueprints.guest import bp as guest_bp
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(device_bp)
app.register_blueprint(guest_bp)

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 设置 uploads 文件夹的静态文件路由
@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory('uploads', filename)

@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}

if __name__ == "__main__":
    app.run(debug=True, port=5000)