import feedparser
import requests
from datetime import datetime
from django.utils import timezone
from main.models import Article, DaylyDijest




# Список источников для парсинга
SOURCES = [
    {
        'name': 'Habr',
        'url': 'https://habr.com/ru/rss/all/',
        'tag': '#Habr'
    },
    {
        'name': 'Dev.to',
        'url': 'https://dev.to/feed/',
        'tag': '#DevTo'
    },
    {
        'name': 'Python Insider',
        'url': 'https://feeds.feedburner.com/PythonInsider',
        'tag': '#Python'
    },
    {
        'name': 'Django Blog',
        'url': 'https://www.djangoproject.com/rss/weblog/',
        'tag': '#Django'
    },
]

def fetch_articles_from_rss():
    """Собирает свежие статьи из RSS-лент"""
    articles = []
    for source in SOURCES:
        try:
            feed = feedparser.parse(source['url'])
            for entry in feed.entries[:5]:  # берём по 5 последних из каждого источника
                # Парсим дату публикации
                pub_date = datetime(*entry.published_parsed[:6])
                # Делаем дату "осознанной" (timezone-aware)
                if timezone.is_naive(pub_date):
                    pub_date = timezone.make_aware(pub_date)
                
                articles.append({
                    'title': entry.title,
                    'url': entry.link,
                    'source': source['name'],
                    'published_at': pub_date,
                })
        except Exception as e:
            print(f"Ошибка парсинга {source['name']}: {e}")
    return articles


def save_articles_to_db(articles):
    """Сохраняет статьи в БД, пропуская дубликаты по URL"""
    saved_count = 0
    for data in articles:
        article, created = Article.objects.get_or_create(
            url=data['url'],
            defaults={
                'title': data['title'],
                'source': data['source'],
                'published_at': data['published_at'],
            }
        )
        if created:
            saved_count += 1
    return saved_count


def get_deepseek_digest(articles):
    """Отправляет заголовки статей в DeepSeek и получает связный дайджест"""
    import os
    from openai import OpenAI  # или используйте requests для совместимости

    # Если у вас установлена библиотека openai
    client = OpenAI(
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com/v1"  # или другой endpoint
    )
    
    # Формируем список заголовков для AI
    titles = "\n".join([f"- {a.title}" for a in articles])
    
    prompt = f"""
    Ты — редактор IT-новостей. Напиши краткий дайджест (3-5 предложений) 
    на основе этих заголовков. Выдели самое важное и интересное.
    
    Заголовки новостей за последний час:
    {titles}
    
    Дайджест:
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Ты — профессиональный редактор IT-новостей. Пиши кратко и по делу."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка DeepSeek: {e}")
        # Фолбэк: просто склеиваем заголовки
        return "\n".join([f"- {a.title}" for a in articles[:5]])