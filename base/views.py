import modules
import django

from django.conf import settings

from selenium import webdriver
from pyvirtualdisplay import Display

from base.models import Detail, RailwayPosition
from django.views.generic import TemplateView
from django.http import HttpResponse

class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):

        context = super(Index, self).get_context_data(*args, **kwargs)
      
        objects = Detail.objects.filter(status__in=['U', 'P']).order_by('status', 'pt_duration', '-estimated_speed', 'bathrooms')

        context["choice_types"] = Detail.DETAIL_CHOICE
        context["REURL"] = settings.REAL_ESTATE_URL
        context["details"] = objects
        context["request"] = self.request
        context["token"] = django.middleware.csrf.get_token(self.request)

        return context

    def post(self, request, *args, **kwargs):
        id = int(request.POST.get('id'))
        val = str(request.POST.get('val'))

        detail = Detail.objects.get(id=id)
        detail.status = val
        detail.save()

        return HttpResponse("")