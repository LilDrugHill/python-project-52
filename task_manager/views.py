from django.views.generic.base import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):

    def greetings(request):
        return render(request, 'index.html', context={'who': 'World'})