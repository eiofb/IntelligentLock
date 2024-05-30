from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from .forms import GuestForm
from models import DeviceModel, PermissionType, GuestModel
from exts import db
from decorators import login_required

bp = Blueprint("guest", __name__, url_prefix="/guest")

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
        name = form.name
        image_path = form.image_path
        access = form.access
        guest = GuestModel(name=name, image_path=image_path, access=PermissionType(access))
        db.session.add(guest)
        db.session.commit()
        return jsonify({"code": 200, "message": "", "data": None})
    else:
        print(form.errors)
        return jsonify({"code": 500, "message": "", "data": form.errors})
        
