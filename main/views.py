from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class MainView(TemplateView):
    template_name = 'main/index.html'




class AboutView(TemplateView):
    template_name = 'main/about.html'
    
