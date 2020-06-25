import dj_database_url
from .settings import * # 含入原本的settings.py所有設定
# heroku使用的資料庫為PostgreSQL，所以要修改資料庫設定
DATABASES = {
    'default': dj_database_url.config(),
}
STATIC_ROOT = 'staticfiles' # 設定網站正式上線時靜態檔案目錄位置
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # 設定HTTP連線方式
ALLOWED_HOSTS = ['*'] # 讓所有的網域都能瀏覽本網站
DEBUG = False # 關閉除錯模式
