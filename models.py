from exts import db
from datetime import datetime
from enum import Enum

# 管理员
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

# 验证码
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(100), nullable=False)

# 设备
class DeviceStatus(Enum):         
    normal = "normal"       
    fault = "fault"

class DeviceModel(db.Model):
    __tablename__ = "device"
    id = db.Column(db.String(100), primary_key=True, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    remaining_power = db.Column(db.Float, default=1.00)
    status = db.Column(db.Enum(DeviceStatus), nullable=False, default=DeviceStatus("normal"))

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="devices")

# 访客
class PermissionType(Enum):
    admin = 'admin'
    guest = 'guest'

class GuestModel(db.Model):
    __tablename__ = "guest"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    image_name = db.Column(db.String(100), nullable=False, unique=True)
    access = db.Column(db.Enum(PermissionType), nullable=False)

    device_id = db.Column(db.String(100), db.ForeignKey("device.id"))
    device = db.relationship(DeviceModel, backref=db.backref("guests"))

# 设备记录
class DeviceRecordModel(db.Model):
    __tablename__ = "device_record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_name = db.Column(db.String(100), nullable=False, unique=True)
    open_type = db.Column(db.Integer, default=0)
    last_open_time = db.Column(db.DateTime, default=datetime.now)

    device_id = db.Column(db.String(100), db.ForeignKey("device.id"))
    device = db.relationship(DeviceModel, backref=db.backref("records", order_by=last_open_time.desc()))
    guest_id = db.Column(db.Integer, db.ForeignKey("guest.id"))
    guest = db.relationship(GuestModel, backref=db.backref("records", order_by=last_open_time.desc()))