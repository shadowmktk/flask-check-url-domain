# flask-check-url-domain
检测URL状态和域名证书的简单示例

# 配置环境变量
Flask和Celery的数据库必须是同一个，否则没法获取到异步任务的返回结果。
```
FLASK_APP_ENVIRONMENT=production
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:123456@192.168.3.106:3306/celery?charset=utf8mb4
CELERY_BROKER_URL=redis://192.168.3.106:6379/0
CELERY_RESULT_BACKEND=db+mysql+pymysql://root:123456@192.168.3.106:3306/celery?charset=utf8mb4
```

# 检查URL状态的API接口
创建URL，需要提交url参数，以`http://`或`https://`开头。非80或443端口，在URL结尾加端口，例如 `https://www.example.org:8443`
```
POST /api/v1/check_url_create

curl -XPOST http://192.168.3.106:8000/api/v1/check_url_create --header 'Content-Type: application/json' --data '{"url": "https://www.python.org"}'
curl -XPOST http://192.168.3.106:8000/api/v1/check_url_create --header 'Content-Type: application/json' --data '{"url": "https://www.example.org:8443"}'
```
获取URL列表
```
POST /api/v1/check_domain_list

curl -XPOST http://192.168.3.106:8000/api/v1/check_domain_list
```
提交异步任务（不需要提交参数），返回`task_id`
```
POST /api/v1/tasks/check_url_status

curl -XPOST http://192.168.3.106:8000/api/v1/tasks/check_url_status
```
# 检查域名证书的API接口
创建域名，需要提交domain和port参数，domain可以是IP或域名，不能以`http://`或`https://`开头。
```
POST /api/v1/check_domain_create

curl http://192.168.3.106:8000/api/v1/check_domain_create --header 'Content-Type: application/json' --data '{"domain": "www.python.org", "port": 443}'
```
获取URL列表
```
POST /api/v1/check_domain_list

curl -XPOST http://192.168.3.106:8000/api/v1/check_domain_list
```
提交异步任务（不需要提交参数），返回`task_id`
```
POST /api/v1/tasks/check_domain_certificate

curl -XPOST http://192.168.3.106:8000/api/v1/tasks/check_domain_certificate
```
# 获取Celery异步任务的API接口
获取所有任务列表
```
POST /api/v1/tasks

curl -XPOST http://192.168.3.106:8000/api/v1/tasks
```
获取单个任务详情
```
GET /api/v1/tasks/<task_id>

curl http://192.168.3.106:8000/api/v1/tasks/5acec2f9-4266-41e6-b872-d1656c1b4dba
```


