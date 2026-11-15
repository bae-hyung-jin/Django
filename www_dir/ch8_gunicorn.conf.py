from pathlib import Path

# [2026-11-15 수정] www_dir/ 이동에 맞춰 프로젝트 루트를 parent.parent로 조정
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

wsgi_app = 'mysite.wsgi'
# bind = '0:8081'
bind = 'unix:/tmp/gunicorn.sock'
daemon = True
accesslog = str(LOG_DIR / 'access.log')
errorlog = str(LOG_DIR / 'error.log')





