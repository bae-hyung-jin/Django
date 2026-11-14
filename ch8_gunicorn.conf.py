# gunicorn config for ch8 project
wsgi_app = 'mysite.wsgi'
# bind = '0:8081'
bind = 'unix:/tmp/gunicorn.sock'
daemon = True
accesslog = '/home/hyungjin/pyBook/ch8/logs.access.log'
errlog = '/home/hyungjin/pyBook/ch8/logs/error.log'

