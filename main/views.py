from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import DaylyDijest
from .tasks import generate_digest

# Create your views here.



class MainView(TemplateView):
    template_name = 'main/index.html'

    latest_digest = DaylyDijest.objects.filter(is_published=True).order_by('-created_at').first()
    articles = []
    
    if latest_digest:
        articles = latest_digest.articles.all()[:10]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["digest"] = self.latest_digest
        context["articles"] = self.articles

        return context
    


def refresh_digest(request):
    """Запускает обновление дайджеста в фоне"""
    generate_digest.delay()
    return JsonResponse({'status': 'ok', 'message': 'Дайджест обновляется...'})




class AboutView(TemplateView):
    template_name = 'main/about.html'
    
