# URL Shortener Django Project (sample)

這是一個小的Django專案，練習了第三方登入以及縮網址的使用


## 功能特色
- Google / Facebook 第三方登入
- 快速建立短網址
- 點擊統計與來源 IP 追蹤
- 個人化管理介面

## 技術架構
- Backend: Django 4.2
- Authentication: django-allauth
- Database: SQLite (開發) / PostgreSQL (生產)
- Frontend: Bootstrap 5

## 本地開發

### 1. 安裝依賴
```
pip install -r requirements.txt
```

### 2. 設定環境變數
建立 `.env` 檔案：
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_secret
FACEBOOK_CLIENT_ID=your_facebook_client_id
FACEBOOK_CLIENT_SECRET=your_facebook_secret
如果有用雲端資料庫:
DB_ENGINE=your-backend-engine
DB_NAME=your-DB-name
DB_USER=your-user-name
DB_PASSWORD=your-password
DB_HOST=your-host
DB_PORT=your-port

### 3. 資料庫遷移
```
python manage.py migrate
```

### 4. 建立超級使用者
```
python manage.py createsuperuser
```

### 5. 啟動開發伺服器
```
python manage.py runserver
```

## OAuth 設定

### Google OAuth
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立專案並啟用 Google+ API
3. 設定 OAuth 同意畫面
4. 建立 OAuth 2.0 用戶端 ID
5. 授權重新導向 URI: `http://localhost:8000/accounts/google/login/callback/`

### Facebook OAuth
1. 前往 [Facebook Developers](https://developers.facebook.com/)
2. 建立應用程式
3. 新增 Facebook Login 產品
4. 設定有效的 OAuth 重新導向 URI: `http://localhost:8000/accounts/facebook/login/callback/`

## 專案結構
urlshortener_project/
├── shortener/          # 主要應用程式\
│   ├── forms.py        # 表格邏輯\
│   ├── models.py       # 資料模型\
│   ├── views.py        # 短網址邏輯\
│   ├── urls.py         # URL 路由\
│   └── templates/      # 短網址相關操作模板檔案\
├── urlshortener/       # 專案設定\
│   ├── settings.py     # 基本設定\
│   ├── urls.py         # URL 路由\
│   └── wsgi.py         # wsgi設定\
├── templates/          # 登入頁面模板\
├── static/             # 靜態檔案放置處\
├── manage.py\
├── requirements.txt\
└── README.md