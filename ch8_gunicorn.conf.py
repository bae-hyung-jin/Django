from pathlib import Path

# [2026-11-15 수정] 교재(예제 8-5) 형식으로 단순화 + 상대 경로(logs/) 적용
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

wsgi_app = 'mysite.wsgi'
# bind = '0:8081'
bind = 'unix:/tmp/gunicorn.sock'
daemon = True
accesslog = str(LOG_DIR / 'access.log')
errorlog = str(LOG_DIR / 'error.log')





