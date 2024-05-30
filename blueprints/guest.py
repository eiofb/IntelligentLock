from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from .forms import DeviceForm
from models import DeviceModel, DeviceRecordModel
from exts import db
from decorators import login_required

bp = Blueprint("guest", __name__, url_prefix="/guest")

# 白名单
@bp.route("/whiter_list/<device_id>")
def white_list(device_id):
    device = DeviceModel.query.filter_by(id=device_id).first()
    return render_template("white_list.html", device=device)