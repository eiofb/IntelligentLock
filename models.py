from exts import db
from datetime import datetime
from enum import Enum

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(100), nullable=False)

class DeviceModel(db.Model):
    __tablename__ = "device"
    id = db.Column(db.String(100), primary_key=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    remaining_power = db.Column(db.Float, default=1.00)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="devices")

class DeviceRecordModel(db.Model):
    __tablename__ = "device_record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_type = db.Column(db.Integer, default=0)
    last_open_time = db.Column(db.DateTime, default=datetime.now)

    device_id = db.Column(db.String(100), db.ForeignKey("device.id"))
    device = db.relationship(DeviceModel, backref=db.backref("records", order_by=last_open_time.desc()))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref=db.backref("records", order_by=last_open_time.desc()))
    
# 白名单
class PermissionType(Enum):
    ADMIN = 'admin'
    GUEST = 'guest'

class WhiteList(db.Model):
    __tablename__ = "white_list"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(100), nullable=False, unique=True)
    acess = db.Column(db.Enum(PermissionType), nullable=False)