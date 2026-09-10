from celery import shared_task
from django.utils import timezone
from .models import DaylyDijest, Article
from .utils import fetch_articles_from_rss, get_deepseek_digest_from_titles
# def generate_digest():
#     """Главная задача: парсим новости, генерируем дайджест, сохраняем"""
    
#     # 1. Парсим RSS
#     articles_data = fetch_articles_from_rss()
#     if not articles_data:
#         return "Нет новых статей"
    
#     # 2. Сохраняем в БД
#     saved_count = save_articles_to_db(articles_data)
    
#     # 3. Берём последние 10 статей для дайджеста
#     recent_articles = Article.objects.order_by('-published_at')[:10]
#     if not recent_articles:
#         return "Нет статей в БД"
    
#     # 4. Генерируем текст через DeepSeek
#     digest_text = get_deepseek_digest(recent_articles)
    
#     # 5. Создаём новый дайджест в БД
#     digest = DaylyDijest.objects.create(
#         title="IT-Дайджест",
#         summary=digest_text,
#         is_published=True
#     )
    
#     # 6. Привязываем статьи к дайджесту (через ManyToMany или ForeignKey)
#     # Если у вас ForeignKey, нужно обновить статьи:
#     for article in recent_articles:
#         article.digest = digest
#         article.save()
    
#     return f"Дайджест создан! Добавлено {saved_count} новых статей"

# tasks.py

@shared_task
def generate_digest():
    """Главная задача: парсим новости, создаем дайджест, сохраняем"""
    
    # 1. Парсим RSS (получаем список словарей, НЕ сохраняем в БД)
    articles_data = fetch_articles_from_rss()
    if not articles_data:
        return "Нет новых статей"
    
    # 2. Генерируем текст дайджеста на основе заголовков
    digest_text = get_deepseek_digest_from_titles(articles_data)
    
    # 3. СОЗДАЕМ ДАЙДЖЕСТ (теперь у него есть ID в БД!)
    digest = DaylyDijest.objects.create(
        title="IT-Дайджест",
        summary=digest_text,
        is_published=True
    )
    
    # 4. Теперь сохраняем статьи и привязываем к digest
    saved_count = 0
    for data in articles_data[:4]:  # берем первые 4
        article, created = Article.objects.get_or_create(
            url=data['url'],
            defaults={
                'title': data['title'],
                'source': data['source'],
                'published_at': data['published_at'],
                'digest': digest,  # ← ВОТ ТЕПЕРЬ ЕСТЬ digest!
            }
        )
        if created:
            saved_count += 1
    
    return f"Дайджест создан! Добавлено {saved_count} новых статей"