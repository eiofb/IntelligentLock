from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from .forms import DeviceForm
from models import DeviceModel, DeviceRecordModel
from exts import db
from decorators import login_required

bp = Blueprint("device", __name__, url_prefix="/")

@bp.route("/")
def index():
    return render_template("index.html")

# 搜索设备ID
@bp.route("/search")
@login_required
def search():
    q = request.args.get("q")
    device_list = DeviceModel.query.filter(DeviceModel.id.contains(q)).all()
    return render_template("device_list.html", device_list=device_list)

# 设备详情页
@bp.route("/device/device_detail/<device_id>")
def device_detail(device_id):
    device = DeviceModel.query.filter_by(id=device_id).first()
    return render_template("device_detail.html", device=device)

# 设备列表
@bp.route("/device/devicelist")
@login_required
def deviceList():
    device_list = g.user.devices
    return render_template("device_list.html",device_list=device_list)

# 添加设备页
@bp.route("/device/addDevice", methods=["GET", "POST"])
@login_required
def addDevice():
    if request.method == "GET":
        return render_template("add_device.html")
    else:
        form = DeviceForm(request.form)
        if form.validate():
            device_id = form.device_id.data
            device_name = form.device_name.data
            device = DeviceModel(device_name=device_name, id=device_id, author=g.user)
            db.session.add(device)
            db.session.commit()
            return jsonify({"code": 200, "message": "", "data": None})
        else:
            print(form.errors)
            return jsonify({"code": 500, "message": "", "data": form.errors})

# 修改设备
@bp.post("/device/modify")
def modify_device():
    form = DeviceForm(request.form)
    if len(form.device_name.data) < 3 or len(form.device_name.data) > 100:
        print("设备名称错误！")
    else:
        device_id = form.device_id.data
        input_name = form.device_name.data
        device = DeviceModel.query.filter_by(id=device_id).first()
        device.device_name = input_name
        db.session.commit()

    return redirect(url_for("device.deviceList"))

# 删除设备
@bp.route("/device/delete_device")
def delete_device():
    # 删除设备下的记录
    device_id = request.args.get("device_id")
    db.session.query(DeviceRecordModel).filter_by(device_id=device_id).delete()

    # 删除设备
    device = DeviceModel.query.filter_by(id=device_id).first()
    db.session.delete(device)

    db.session.commit()
    return jsonify({"code": 200, "message": "", "data": None})
