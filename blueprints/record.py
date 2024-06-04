from flask import Blueprint, request, jsonify
from models import GuestModel, DeviceRecordModel, DeviceModel
from exts import db
from datetime import datetime
from decorators import allowed_file, generate_captcha
import os, config, requests

bp = Blueprint("record", __name__, url_prefix="/record")

# 添加新记录
@bp.post("/add_record")
def add_record():
    # 获取表单数据
    form_data = request.form
    name = form_data['name']
    confidence = form_data['confidence']
    device_id = form_data['device_id']

    # 置信度低于阈值不开锁
    if confidence < config.confidence_threshold:
        return jsonify({"code": 200, "message": "置信度低于阈值", "data": None})

    # 名字不在白名单中不开锁
    guest = GuestModel.query.filter_by(name=name).first()
    if not guest:
        return jsonify({"code": 200, "message": "不在白名单中", "data": None})

    # 发送开锁指令
    response = requests.get(config.ESP8266_url)
    if response.status_code == 200:

        # 保存图片到服务器
        if 'record_img' not in request.files:
            print('没有文件部分')
        file = request.files['record_img']
        if file.filename == '':
            print('没有选择文件')
        if file and allowed_file(file.filename):

            # 文件名不能重复
            filename = file.filename
            extend = '.' + filename.rsplit('.', 1)[1]
            while os.path.exists(os.path.join(config.RECORD_FOLDER, filename)):
                filename = filename.rsplit('.', 1)[0] + generate_captcha + extend
            file.save(os.path.join(config.RECORD_FOLDER, file.filename))

            # 保存记录
            device = DeviceModel.query.filter_by(device_id=device_id).first()
            record = DeviceRecordModel(image_name=filename, last_open_time=datetime.now(), open_type=0, device=device, guest=guest)
            db.session.add(record)
            db.session.commit()
            print('文件已成功上传')
        else:
            print('不允许的文件类型')
    else:
        print("请求失败，状态码：", response.status_code)
