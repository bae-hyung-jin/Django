# Django Study Project WBS

Django 수업 실습을 기반으로 Bookmark, Blog, Photo 기능을 통합한 웹 애플리케이션입니다.

## 이번 수정 내역

### 실행 환경 및 설정

- `requirements.txt`
  - `django-taggit`, `django-taggit-templatetags2`, `django-widget-tweaks`, `Pillow` 의존성 추가
- `mysite/settings.py`
  - 잘못된 `MAILERS` 설정을 `EMAIL_BACKEND`로 수정
  - `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` 환경 변수 지원

### 모델 및 게시글

- `bookmark/models.py`
  - 존재하지 않는 `modify_dt`를 참조하던 이전·다음 메서드 제거
- `blog/models.py`
  - 게시글 생성 시에만 slug를 자동 생성하도록 수정
- `blog/views.py`
  - 게시글 생성·수정 폼에서 사용자가 slug를 직접 입력하지 않도록 수정
- `blog/templates/blog/post_form.html`
  - 제거된 slug 입력 영역 삭제

### 사진 및 URL

- `photo/views.py`
  - 중복 `PhotoDV` 클래스 제거
  - 사진 생성·수정 시 현재 사용자의 앨범만 선택 가능하도록 제한
- `photo/urls.py`
  - 사진 생성 URL에 trailing slash 추가

### 문서 및 저장소 정리

- `README.md`
  - WBS, 실행 방법, 운영 환경 설정, 이번 수정 내역 추가
- `__MACOSX/`
  - Git에 포함되어 있던 macOS 메타파일 제거

## 1. 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| 프로젝트명 | Django Study Project |
| 목적 | Django의 모델, URL, 클래스형 뷰, 인증, 관리자 기능 학습 |
| 주요 기술 | Python, Django, SQLite, Pillow |
| 대상 사용자 | 회원가입 후 게시글·북마크·사진을 관리하는 사용자 |

## 2. 작업 분해 구조(WBS)

### 2.1 프로젝트 기반 구성

- Django 프로젝트 및 앱 구조 구성
- 공통 설정 및 URL 라우팅 구성
- 템플릿 상속 구조와 정적 파일 구성
- SQLite 데이터베이스 및 마이그레이션 관리

### 2.2 사용자 인증

- 회원가입 및 로그인 구현
- 로그아웃 및 비밀번호 변경 구현
- 로그인 사용자만 생성·수정·삭제 기능 사용
- 객체 소유자만 수정·삭제할 수 있도록 권한 검증

### 2.3 Bookmark 기능

- 북마크 모델 및 URL 필드 구성
- 북마크 목록·상세 화면 구현
- 북마크 생성·수정·삭제 구현
- 사용자별 북마크 관리 목록 구현

### 2.4 Blog 기능

- 게시글 모델 및 태그 기능 구성
- 게시글 목록·상세 화면 구현
- 연도·월·일·오늘 기준 아카이브 구현
- 태그 클라우드 및 태그별 게시글 조회 구현
- 게시글 검색 구현
- 게시글 생성·수정·삭제 및 작성자 권한 관리
- Disqus 댓글 연동

### 2.5 Photo 기능

- 앨범 및 사진 모델 구성
- 이미지 업로드와 썸네일 생성 구현
- 앨범·사진 목록 및 상세 화면 구현
- 앨범과 사진을 함께 생성·수정하는 인라인 폼셋 구현
- 사용자별 앨범·사진 관리 및 소유권 검증

### 2.6 운영 및 품질 관리

- 환경 변수를 통한 비밀키·디버그·허용 호스트 관리
- 정적 파일 및 미디어 파일 설정
- 패키지 의존성 관리
- Django 시스템 검사 및 마이그레이션 검사
- 테스트 코드 확장

## 3. 현재 구현 상태

| 작업 영역 | 상태 |
| --- | --- |
| 프로젝트 기본 구조 | 완료 |
| 인증 및 회원 관리 | 완료 |
| Bookmark CRUD | 완료 |
| Blog CRUD·검색·아카이브 | 완료 |
| 태그 및 Disqus 연동 | 완료 |
| Photo 앨범·업로드·썸네일 | 완료 |
| 소유자 권한 검증 | 완료 |
| 자동화 테스트 확장 | 진행 예정 |
| 운영 환경 배포 | 진행 예정 |

## 4. 개발 환경

- Python 3.14
- Django 6.1
- SQLite
- macOS
- Visual Studio Code

## 5. 실행 방법

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

개발 서버 주소: <http://127.0.0.1:8000/>

관리자 계정은 다음 명령으로 생성할 수 있습니다.

```bash
python manage.py createsuperuser
```

## 6. 운영 환경 설정

운영 환경에서는 개발용 기본값을 사용하지 말고 다음 환경 변수를 설정합니다.

```bash
export DJANGO_SECRET_KEY='change-this-secret'
export DJANGO_DEBUG='False'
export DJANGO_ALLOWED_HOSTS='example.com'
```

미디어 파일을 업로드하는 경우 운영 서버에서 `MEDIA_ROOT`를 별도로 관리하고,
정적 파일 배포 전에 다음 명령을 실행합니다.

```bash
python manage.py collectstatic
```
