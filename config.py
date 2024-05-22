SECRET_KEY = ";oiasd,sopdeewf"

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