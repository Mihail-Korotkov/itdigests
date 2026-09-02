from django.contrib import admin

# Register your models here.
from  main.models import DaylyDijest
from main.models import Article

@admin.register(DaylyDijest)
class DaylyDijestAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at','is_published')
    search_fields = ('title',)
    list_filter = ('is_published',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'published_at')
    search_fields = ('title',)





