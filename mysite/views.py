# [2026-11-17] API 적용 전으로 되돌리기 위해 주석 처리 (카카오 키/사고다발 DB 사용 부분)
# import os

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

# from walkmap.models import AccidentSpot


class HomeView(TemplateView):
    template_name = 'home.html'

    #     def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs)
    #         context['kakao_js_key'] = os.environ.get('KAKAO_JS_KEY', '')
    #         context['spots'] = list(
    #             AccidentSpot.objects.values(
    #                 'id', 'year', 'gu_name', 'spot_nm',
    #                 'occrrnc_cnt', 'caslt_cnt', 'dth_dnv_cnt', 'lat', 'lng'
    #             )
    #         )
    #         return context


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
