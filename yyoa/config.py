# 存放配置信息

# mysql数据库的配置信息
HOSTNAME = "127.0.0.1"  # ip地址
PORT = 3306  # 端口号
USERNAME = "root"  # 用户名
PASSWORD = "root"  # 密码
DATABASE = "yyoa"  # 数据库名字
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 发件邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "892901548@qq.com"
MAIL_PASSWORD = "frpofgqbeknkbdji"
MAIL_DEFAULT_SENDER = "892901548@qq.com"
