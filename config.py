SECRET_KEY = ";oiasd,sopdeewf"
UPLOAD_FOLDER = 'uploads/'
RECORD_FOLDER = 'records/'
confidence_threshold = 0.8
ESP8266_url = 'http://127.0.0.1:7890'  # 替换为ESP8266端口

HOSTNAME = "127.0.0.1"
PORT = 3306
DATABASE = "intelligent_lock"
USERNAME = "root"
PASSWORD = "root"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "719304290@qq.com"
MAIL_PASSWORD = "wpnjlnrmbzybbddh"
MAIL_DEFAULT_SENDER = "719304290@qq.com"

# 此处定义锁的状态
open = 0b000001
normal = 0b000010
received = 0b000100
executed = 0b001000