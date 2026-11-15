from pathlib import Path
import os

# [2026-11-15 수정] Gunicorn 배포 경로 및 설정 오류(logs.access.log, errlog) 수정
# - 리눅스 절대 경로(/home/hyungjin/pyBook/ch8) 제거 → 프로젝트 기준 상대 경로(logs/)로 변경
# - GUNICORN_LOG_DIR, GUNICORN_BIND, GUNICORN_DAEMON 환경변수 지원 추가
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = Path(os.environ.get("GUNICORN_LOG_DIR", BASE_DIR / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)  # logs 폴더가 없으면 자동 생성

wsgi_app = "mysite.wsgi"  # Django WSGI 진입점
bind = os.environ.get("GUNICORN_BIND", "unix:/tmp/gunicorn.sock")  # Nginx 연동 Unix 소켓
daemon = os.environ.get("GUNICORN_DAEMON", "True").lower() in ("1", "true", "yes")
accesslog = str(LOG_DIR / "access.log")  # [2026-11-15 수정] logs.access.log → logs/access.log
errorlog = str(LOG_DIR / "error.log")    # [2026-11-15 수정] errlog 오타 → errorlog




