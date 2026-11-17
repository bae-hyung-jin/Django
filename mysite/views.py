# [2026-11-17] API 적용 전으로 되돌리기 위해 주석 처리 (카카오 키/사고다발 DB 사용 부분)
import os,requests

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

# from walkmap.models import AccidentSpot


class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kakao_js_key'] = os.environ.get('KAKAO_JS_KEY', '')
        service_key = os.environ.get('DATA_GO_KR_KEY', '')
        url = 'https://apis.data.go.kr/B551011/KorService2/searchKeyword2'
        params = {
            'serviceKey': service_key,
            'MobileOS': 'ETC',
            'MobileApp': 'WalkProject',
            '_type': 'json',
            'keyword': '청주',
            'contentTypeId': 12,  # 12 = 관광지 (숙박/식당 제외)
            'numOfRows': 20,      # 넉넉하게 20개 받아온 뒤
            'pageNo': 1,
        }
        places = []
        try:
            res = requests.get(url, params=params, timeout=5)
            data = res.json()
            items = data['response']['body']['items']['item']
            # 주소에 '청주시'가 들어간 것만 최대 6개 추리기
            places = [p for p in items if '청주시' in p.get('addr1', '')][:6]
        except Exception:
            pass
        context['places'] = places
        return context


class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')


class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update.delete the object."

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object() #type: ignore
        if request.user != obj.owner:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs) #type: ignore
