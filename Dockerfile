FROM python:3.10-slim

# Add variable
ENV FLASK_APP_ENVIRONMENT=production

ENV SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:123456@192.168.3.106:3306/celery?charset=utf8mb4

ENV CELERY_BROKER_URL=redis://192.168.3.106:6379/0

ENV CELERY_RESULT_BACKEND=db+mysql+pymysql://root:123456@192.168.3.106:3306/celery?charset=utf8mb4

# Add Tini
# ARG GITHUB_PROXY=https://ghproxy.com/
# ENV TINI_VERSION v0.19.0
# ADD ${GITHUB_PROXY}https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-static /tini
COPY tini-static .

WORKDIR /app
COPY . /app 

ENV PIP_INDEX_URL https://pypi.tuna.tsinghua.edu.cn/simple
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["/tini-static", "--"]

CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]
