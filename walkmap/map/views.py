# [2026-11-17 추가] 새 사이트 지도 화면의 뷰.
# 원래 walkmap/bookmark/views.py 에 잘못 들어가 있던 MapView 를 이곳으로 옮김.
# (그 파일에는 TemplateView, os, AccidentSpot import 가 없어서 NameError 로 서버 전체가 죽었다)
import os  # .env 에서 읽은 KAKAO_JS_KEY 를 os.environ 으로 꺼내기 위해 필요

from django.views.generic import TemplateView

from walkmap.models import AccidentSpot  # 사고다발 지점 DB 모델


class MapView(TemplateView):
    # 템플릿 위치: walkmap/templates/walkmap/map/map.html
    template_name = 'walkmap/map/map.html'

    # map.html 의 {{ kakao_js_key }}, {{ spots }} 값을 채워서 넘겨준다.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 카카오 지도 SDK 주소의 appkey= 뒤에 들어갈 JavaScript 키 (.env → 환경변수)
        context['kakao_js_key'] = os.environ.get('KAKAO_JS_KEY', '')
        # 지도 마커와 아래 표에 함께 쓰는 사고다발 지점 목록
        context['spots'] = list(
            AccidentSpot.objects.values(
                'id', 'year', 'gu_name', 'spot_nm',
                'occrrnc_cnt', 'caslt_cnt', 'dth_dnv_cnt', 'lat', 'lng'
            )
        )
        return context
