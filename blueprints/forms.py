import wtforms, os
from wtforms.validators import Email, Length, EqualTo
from models import UserModel, EmailCaptchaModel, DeviceModel, PermissionType

class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或者验证码错误！")

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])

# 验证添加设备表单
class DeviceForm(wtforms.Form):
    device_id = wtforms.StringField(validators=[Length(min=3, max=100, message="设备id错误！")])
    device_name = wtforms.StringField(validators=[Length(min=3, max=100, message="设备名称错误！")])

    def validate_device_id(self, field):
        device_id = field.data
        device = DeviceModel.query.filter_by(id=device_id).first()
        if device:
            raise wtforms.ValidationError(message="该设备已存在！")
        
# 验证添加访客表单
class GuestForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=3, max=100, message="设备名称错误！")])
    
    def validate_image_path(self, field):
        image_path = field.data
        if not os.path.exists(image_path):
            raise wtforms.ValidationError(message="文件不存在！")
        
    def validate_access(self, field):
        access = field.data
        if access not in [item.value for item in PermissionType]:
            raise wtforms.ValidationError(message="权限不存在！")