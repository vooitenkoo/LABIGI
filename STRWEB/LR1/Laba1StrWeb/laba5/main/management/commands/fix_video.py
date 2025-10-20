from django.core.management.base import BaseCommand
from main.models import CompanyInfo

class Command(BaseCommand):
    help = 'Исправляет URL видео в базе данных'

    def handle(self, *args, **options):
        # Получаем или создаем информацию о компании
        company_info, created = CompanyInfo.objects.get_or_create(
            name='ООО "Грузоперевозки"',
            defaults={
                'description': '''Мы - ведущая компания в сфере грузоперевозок, 
                предоставляющая полный спектр логистических услуг. 
                Наша миссия - обеспечить надежную и быструю доставку грузов 
                для наших клиентов с использованием современного транспорта 
                и профессиональных водителей.''',
                'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'history': '''Компания была основана в 2010 году с целью 
                предоставления качественных услуг грузоперевозок. 
                За годы работы мы зарекомендовали себя как надежный партнер 
                для множества клиентов.''',
                'requisites': '''ООО "Грузоперевозки"
                УНП: 123456789
                ОКПО: 12345678
                р/с: BY86ALFA30143400000010270000
                в ОАО "Альфа-Банк"
                БИК: ALFABY2X
                Адрес: г. Минск, ул. Примерная, д. 123''',
                'certificate_text': '''Сертификат качества
                Настоящим подтверждается, что ООО "Грузоперевозки"
                соответствует всем требованиям качества и безопасности
                в сфере грузоперевозок.'''
            }
        )
        
        # Обновляем URL видео на указанное пользователем
        company_info.video_url = 'https://www.youtube.com/watch?v=hbseyn-CfXY'
        company_info.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Видео URL обновлен: {company_info.video_url}')
        )
