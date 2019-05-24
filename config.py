WTF_CSRF_ENABLED = False
# WTF_CSRF_ENABLED = True

import os
SECRET_KEY = os.urandom(24) # 利用session存cookie数据的时候会用到

DB_CONFIG = {
    'DRIVER': 'pymysql',
    'USER': 'fury',
    # 'PASSWORD': '182838',
    'PASSWORD': 'YES',
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'NAME': 'test_login',
    # 'NAME': 'test_login',
    'CHARSET': 'utf8'
}
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://fury:182838@127.0.0.1:3306/test_login?charset=utf8'
# SQLALCHEMY_DATABASE_URI = 'mysql+{DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}?charset={CHARSET}'.format(**DB_CONFIG);
