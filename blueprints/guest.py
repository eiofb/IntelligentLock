from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from .forms import GuestForm
from models import DeviceModel, PermissionType, GuestModel
from exts import db
from decorators import login_required
import os, config

bp = Blueprint("guest", __name__, url_prefix="/guest")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 白名单
@login_required
@bp.route("/white_list/<device_id>")
def white_list(device_id):
    permissions = [ptype.value for ptype in PermissionType]
    device = DeviceModel.query.filter_by(id=device_id).first()
    return render_template("white_list.html", device=device, permissions=permissions)

# 添加访客
@bp.post("/add_guest")
def add_guest():
    form = GuestForm(request.form)
    if form.validate():
        name = form.name.data
        access = form.access.data
        device_id = form.device_id.data
        
        # 保存图片到服务器
        if 'upload_image' not in request.files:
            print('没有文件部分')
        file = request.files['upload_image']
        if file.filename == '':
            print('没有选择文件')
        if file and allowed_file(file.filename):
            file.save(os.path.join(config.UPLOAD_FOLDER, file.filename))
            print('文件已成功上传')
        else:
            print('不允许的文件类型')
            
        device = DeviceModel.query.filter_by(id=device_id).first()
        guest = GuestModel(name=name, image_name=file.filename, access=PermissionType(access), device=device)
        db.session.add(guest)
        db.session.commit()
        return jsonify({"code": 200, "message": "", "data": None})
    else:
        print(form.errors)
        return jsonify({"code": 500, "message": "", "data": form.errors})
        
# 删除访客
@bp.route("/delete_guest")
def delete_guest():
    guest_id = request.args.get("guest_id")
    guest = GuestModel.query.filter_by(id=guest_id).first()
    
    # 删除服务器中的图片
    file_path = url_for("uploads", filename=guest.image_name)

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 删除文件
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")
    
    db.session.delete(guest)
    db.session.commit()
    return jsonify({"code": 200, "message": "", "data": None})
