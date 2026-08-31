from tabnanny import verbose

from django.db import models

# Create your models here.
class DaylyDijest(models.Model):
    title = models.CharField(max_length=200, default="IT-Дайджест")
    summary = models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class meta:
        ordering  = ['-created_at']
        verbose_name = 'IT-Дайджест'
        verbose_name_plural = 'IT-Дайджесты'

    def __str__(self):
        return f"Дайджест от {self.created_at.strftime('%d.%m.%Y')}"

class Article(models.Model):
    digist = models.ForeignKey(DaylyDijest, on_delete=models.CASCADE,related_name='articles')
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    source = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    
    class meta:
        ordering  = ['-Published_at']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title