from django.shortcuts import render
from django.views import generic


class IndexPageView(generic.base.TemplateView):

    template_name = 'polls/index.html'
