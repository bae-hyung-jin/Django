# [2026-11-17 수정] 에러 원인 정리
#  1) 12번째 줄 `return context` 들여쓰기가 3칸이라 IndentationError 발생 → 8칸으로 맞춤
#  2) 코드에서 쓰는 os, AccidentSpot을 import 하지 않아 NameError가 날 상태 → import 추가
import os  # [추가] .env에서 읽은 KAKAO_JS_KEY를 os.environ으로 꺼내 쓰기 위해 필요

from django.views.generic import TemplateView

from walkmap.models import AccidentSpot, Crosswalk  # 사고다발 지점 및 횡단보도 DB 모델


# [2026-11-17 추가] 새 사이트의 홈(소개) 화면. /walkmap/ 으로 접속하면 이 뷰가 실행된다.
class WalkmapHomeView(TemplateView):
    template_name = 'walkmap/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kakao_js_key'] = os.environ.get('KAKAO_JS_KEY', '')
        # 사고다발 지점 목록
        context['spots'] = list(
            AccidentSpot.objects.values(
                'id', 'year', 'gu_name', 'spot_nm',
                'occrrnc_cnt', 'caslt_cnt', 'dth_dnv_cnt', 'lat', 'lng'
            )
        )
        # 횡단보도 목록 (위치, 길이, 신호등 유무)
        context['crosswalks'] = list(
            Crosswalk.objects.values(
                'id', 'manage_no', 'road_nm', 'address',
                'length', 'width', 'lanes', 'has_signal', 'lat', 'lng'
            )
        )
        return context
