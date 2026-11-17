# [2026-11-17 수정] 에러 원인 정리
#  1) 12번째 줄 `return context` 들여쓰기가 3칸이라 IndentationError 발생 → 8칸으로 맞춤
#  2) 코드에서 쓰는 os, AccidentSpot을 import 하지 않아 NameError가 날 상태 → import 추가
import os  # [추가] .env에서 읽은 KAKAO_JS_KEY를 os.environ으로 꺼내 쓰기 위해 필요

from django.views.generic import TemplateView

from walkmap.models import AccidentSpot  # [추가] 사고다발 지점 DB 모델


# [2026-11-17 추가] 새 사이트의 홈(소개) 화면. /walkmap/ 으로 접속하면 이 뷰가 실행된다.
class WalkmapHomeView(TemplateView):
    template_name = 'walkmap/home.html'

    # [추가] 템플릿(home.html)의 {{ kakao_js_key }}, {{ spots }} 값을 채워서 넘겨주는 함수.
    # 이전에는 mysite/views.py의 HomeView가 하던 일인데, 지도를 새 홈으로 옮기면서 여기로 옮김.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 카카오 지도 SDK 주소의 appkey= 뒤에 들어갈 JavaScript 키 (.env → 환경변수)
        context['kakao_js_key'] = os.environ.get('KAKAO_JS_KEY', '')
        # 지도에 마커로 찍을 사고다발 지점 목록 (home.html에서 json_script로 JS에 전달)
        context['spots'] = list(
            AccidentSpot.objects.values(
                'id', 'year', 'gu_name', 'spot_nm',
                'occrrnc_cnt', 'caslt_cnt', 'dth_dnv_cnt', 'lat', 'lng'
            )
        )
        return context  # [수정] 들여쓰기 8칸으로 정리 (함수 본문과 같은 칸)
