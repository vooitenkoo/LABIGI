from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """
    Преобразует YouTube URL в embed формат
    """
    if not url:
        return url
    
    # Если уже embed URL
    if 'youtube.com/embed/' in url:
        return url
    
    # Извлекаем ID видео из различных форматов YouTube URL
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    
    return url
