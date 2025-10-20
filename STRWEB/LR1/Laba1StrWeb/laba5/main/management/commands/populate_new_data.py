from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import (
    Banner, Partner, Product, CompanyInfo, CompanyHistory, 
    Dictionary, FAQ, Employee, Vacancy, PromoCode
)
from decimal import Decimal
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Заполняет базу данных новыми тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем заполнение базы данных...')
        
        # Создаем баннеры
        self.create_banners()
        
        # Создаем партнеров
        self.create_partners()
        
        # Создаем товары/услуги
        self.create_products()
        
        # Создаем информацию о компании
        self.create_company_info()
        
        # Создаем историю компании
        self.create_company_history()
        
        # Создаем словарь терминов
        self.create_dictionary()
        
        # Создаем FAQ
        self.create_faq()
        
        # Создаем сотрудников
        self.create_employees()
        
        # Создаем вакансии
        self.create_vacancies()
        
        # Создаем промокоды
        self.create_promocodes()
        
        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена!')
        )

    def create_banners(self):
        banners_data = [
            {
                'title': 'Надежные грузоперевозки',
                'description': 'Доставляем ваши грузы быстро и безопасно',
                'order': 1
            },
            {
                'title': 'Скидка 15% на первый заказ',
                'description': 'Специальное предложение для новых клиентов',
                'order': 2
            },
            {
                'title': 'Работаем 24/7',
                'description': 'Круглосуточная служба доставки',
                'order': 3
            }
        ]
        
        for banner_data in banners_data:
            Banner.objects.get_or_create(
                title=banner_data['title'],
                defaults={
                    'description': banner_data['description'],
                    'order': banner_data['order'],
                    'is_active': True
                }
            )
        
        self.stdout.write('Созданы баннеры')

    def create_partners(self):
        partners_data = [
            {
                'name': 'БелАЗ',
                'description': 'Производитель карьерных самосвалов',
                'website_url': 'https://belaz.by'
            },
            {
                'name': 'МАЗ',
                'description': 'Минский автомобильный завод',
                'website_url': 'https://maz.by'
            },
            {
                'name': 'ГАЗ',
                'description': 'Горьковский автомобильный завод',
                'website_url': 'https://gaz.ru'
            },
            {
                'name': 'Камаз',
                'description': 'Камский автомобильный завод',
                'website_url': 'https://kamaz.ru'
            }
        ]
        
        for partner_data in partners_data:
            Partner.objects.get_or_create(
                name=partner_data['name'],
                defaults={
                    'description': partner_data['description'],
                    'website_url': partner_data['website_url'],
                    'is_active': True
                }
            )
        
        self.stdout.write('Созданы партнеры')

    def create_products(self):
        products_data = [
            {
                'name': 'Грузоперевозки по городу',
                'description': 'Быстрая доставка грузов в пределах города',
                'price': Decimal('50.00'),
                'category': 'Услуга'
            },
            {
                'name': 'Междугородние перевозки',
                'description': 'Доставка грузов между городами',
                'price': Decimal('200.00'),
                'category': 'Услуга'
            },
            {
                'name': 'Упаковка грузов',
                'description': 'Профессиональная упаковка для безопасной транспортировки',
                'price': Decimal('25.00'),
                'category': 'Услуга'
            },
            {
                'name': 'Хранение на складе',
                'description': 'Временное хранение грузов на наших складах',
                'price': Decimal('10.00'),
                'category': 'Услуга'
            },
            {
                'name': 'Страхование груза',
                'description': 'Полное страхование груза на время перевозки',
                'price': Decimal('100.00'),
                'category': 'Услуга'
            },
            {
                'name': 'Экспресс-доставка',
                'description': 'Срочная доставка в течение 2 часов',
                'price': Decimal('150.00'),
                'category': 'Услуга'
            }
        ]
        
        for product_data in products_data:
            Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': product_data['category'],
                    'is_available': True
                }
            )
        
        self.stdout.write('Созданы товары/услуги')

    def create_company_info(self):
        company_info, created = CompanyInfo.objects.get_or_create(
            name='ООО "Грузоперевозки"',
            defaults={
                'description': '''Мы - ведущая компания в сфере грузоперевозок, 
                предоставляющая полный спектр логистических услуг. 
                Наша миссия - обеспечить надежную и быструю доставку грузов 
                для наших клиентов с использованием современного транспорта 
                и профессиональных водителей.''',
                'video_url': 'https://www.youtube.com/watch?v=hbseyn-CfXY',
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
                'certificate_text': '''СЕРТИФИКАТ О ЧЛЕНСТВЕ В РТА (РЕЕСТР ТУРИСТИЧЕСКИХ АГЕНТСТВ) АССОЦИАЦИИ
                ТУРПОМОЩЬ
                
                ЕДИНЫЙ РЕЕСТР ТУРАГЕНТОВ
                СВИДЕТЕЛЬСТВО
                о внесении сведений
                
                г. Минск
                17 января 2025
                
                Общество с ограниченной ответственностью «Грузоперевозки»
                (УНП 123456789)
                Реестровый номер: 8241
                
                Осауленко А.П.
                Директор Ассоциации "ТУРПОМОЩЬ"
                
                Ассоциация "Объединение туроператоров"
                в сфере выездного туризма "ТУРПОМОЩЬ"
                101000, г. Минск, ул. Мясницкая, дом 47
                Тел. +375 (29) 123-45-67
                e-mail: office@cargo.by'''
            }
        )
        
        if created:
            self.stdout.write('Создана информация о компании')

    def create_company_history(self):
        history_data = [
            {'year': 2010, 'event': 'Основание компании ООО "Грузоперевозки"'},
            {'year': 2012, 'event': 'Расширение автопарка до 10 единиц техники'},
            {'year': 2015, 'event': 'Открытие филиала в Гомеле'},
            {'year': 2018, 'event': 'Внедрение системы GPS-мониторинга'},
            {'year': 2020, 'event': 'Запуск онлайн-платформы для заказа услуг'},
            {'year': 2023, 'event': 'Достижение 1000 довольных клиентов'},
            {'year': 2025, 'event': 'Внедрение экологически чистого транспорта'}
        ]
        
        for history_item in history_data:
            CompanyHistory.objects.get_or_create(
                year=history_item['year'],
                defaults={'event': history_item['event']}
            )
        
        self.stdout.write('Создана история компании')

    def create_dictionary(self):
        dictionary_data = [
            {
                'term': 'Грузоперевозки',
                'definition': 'Транспортировка грузов от места отправления до места назначения с использованием различных видов транспорта.'
            },
            {
                'term': 'Логистика',
                'definition': 'Наука о планировании, управлении и контроле движения материальных, информационных и финансовых ресурсов.'
            },
            {
                'term': 'Экспедирование',
                'definition': 'Организация перевозки грузов, включающая оформление документов, контроль за движением груза.'
            },
            {
                'term': 'Тоннаж',
                'definition': 'Грузоподъемность транспортного средства, выраженная в тоннах.'
            },
            {
                'term': 'Транзит',
                'definition': 'Перевозка грузов через территорию страны без выгрузки и перегрузки.'
            }
        ]
        
        for dict_item in dictionary_data:
            Dictionary.objects.get_or_create(
                term=dict_item['term'],
                defaults={'definition': dict_item['definition']}
            )
        
        self.stdout.write('Создан словарь терминов')

    def create_faq(self):
        faq_data = [
            {
                'question': 'Как оформить заказ на грузоперевозку?',
                'answer': 'Для оформления заказа вы можете воспользоваться нашим сайтом, позвонить по телефону или посетить наш офис. Необходимо указать тип груза, адреса отправления и назначения, желаемую дату перевозки.'
            },
            {
                'question': 'Какие документы нужны для перевозки?',
                'answer': 'Для перевозки груза необходимы документы, удостоверяющие личность отправителя и получателя, документы на груз (накладная, сертификат качества и т.д.), а также документы на транспортное средство.'
            },
            {
                'question': 'Сколько стоит доставка?',
                'answer': 'Стоимость доставки зависит от расстояния, веса и объема груза, типа транспорта и срочности. Точную стоимость вы можете узнать, оставив заявку на нашем сайте или позвонив по телефону.'
            },
            {
                'question': 'Можно ли отследить груз в пути?',
                'answer': 'Да, мы предоставляем возможность отслеживания груза в режиме реального времени через нашу систему GPS-мониторинга.'
            },
            {
                'question': 'Предоставляете ли вы страховку груза?',
                'answer': 'Да, мы предлагаем полное страхование груза на время перевозки. Стоимость страхования рассчитывается индивидуально в зависимости от стоимости груза.'
            }
        ]
        
        for faq_item in faq_data:
            FAQ.objects.get_or_create(
                question=faq_item['question'],
                defaults={'answer': faq_item['answer']}
            )
        
        self.stdout.write('Созданы FAQ')

    def create_employees(self):
        employees_data = [
            {
                'name': 'Иван Петров',
                'position': 'Генеральный директор',
                'description': 'Руководит деятельностью компании, принимает стратегические решения',
                'phone': '+375 (29) 123-45-67',
                'email': 'director@cargo.by'
            },
            {
                'name': 'Мария Сидорова',
                'position': 'Менеджер по работе с клиентами',
                'description': 'Консультирует клиентов, оформляет заказы, решает вопросы по доставке',
                'phone': '+375 (29) 123-45-68',
                'email': 'manager@cargo.by'
            },
            {
                'name': 'Алексей Козлов',
                'position': 'Логист',
                'description': 'Планирует маршруты, координирует работу водителей, контролирует сроки доставки',
                'phone': '+375 (29) 123-45-69',
                'email': 'logist@cargo.by'
            },
            {
                'name': 'Елена Морозова',
                'position': 'Бухгалтер',
                'description': 'Ведет финансовый учет, оформляет документы, работает с поставщиками',
                'phone': '+375 (29) 123-45-70',
                'email': 'accountant@cargo.by'
            }
        ]
        
        for emp_data in employees_data:
            Employee.objects.get_or_create(
                name=emp_data['name'],
                defaults={
                    'position': emp_data['position'],
                    'description': emp_data['description'],
                    'phone': emp_data['phone'],
                    'email': emp_data['email'],
                    'is_active': True
                }
            )
        
        self.stdout.write('Созданы сотрудники')

    def create_vacancies(self):
        vacancies_data = [
            {
                'title': 'Водитель категории C',
                'description': 'Требуется водитель для работы на грузовом автомобиле. Опыт работы от 2 лет.',
                'requirements': 'Права категории C, стаж вождения от 2 лет, знание города, ответственность',
                'salary': 'от 1500 BYN',
                'location': 'Минск'
            },
            {
                'title': 'Менеджер по продажам',
                'description': 'Приглашаем активного менеджера для работы с клиентами и развития продаж.',
                'requirements': 'Высшее образование, опыт работы в продажах от 1 года, коммуникабельность',
                'salary': 'от 1200 BYN + премии',
                'location': 'Минск'
            },
            {
                'title': 'Логист',
                'description': 'Требуется специалист для планирования маршрутов и координации перевозок.',
                'requirements': 'Опыт работы в логистике, знание программ планирования, аналитическое мышление',
                'salary': 'от 1300 BYN',
                'location': 'Минск'
            }
        ]
        
        for vac_data in vacancies_data:
            Vacancy.objects.get_or_create(
                title=vac_data['title'],
                defaults={
                    'description': vac_data['description'],
                    'requirements': vac_data['requirements'],
                    'salary': vac_data['salary'],
                    'location': vac_data['location'],
                    'is_active': True
                }
            )
        
        self.stdout.write('Созданы вакансии')

    def create_promocodes(self):
        promocodes_data = [
            {
                'code': 'WELCOME15',
                'description': 'Скидка 15% на первый заказ для новых клиентов',
                'discount_percent': Decimal('15.00'),
                'status': 'active'
            },
            {
                'code': 'SUMMER2025',
                'description': 'Летняя акция - скидка 20% на все услуги',
                'discount_percent': Decimal('20.00'),
                'status': 'active'
            },
            {
                'code': 'FREESHIP',
                'description': 'Бесплатная доставка при заказе от 200 BYN',
                'discount_amount': Decimal('50.00'),
                'status': 'active'
            },
            {
                'code': 'OLD2024',
                'description': 'Старый промокод (в архиве)',
                'discount_percent': Decimal('10.00'),
                'status': 'archived'
            }
        ]
        
        for promo_data in promocodes_data:
            PromoCode.objects.get_or_create(
                code=promo_data['code'],
                defaults={
                    'description': promo_data['description'],
                    'discount_percent': promo_data.get('discount_percent', Decimal('0.00')),
                    'discount_amount': promo_data.get('discount_amount', Decimal('0.00')),
                    'status': promo_data['status'],
                    'start_date': datetime.now(),
                    'end_date': datetime.now() + timedelta(days=30)
                }
            )
        
        self.stdout.write('Созданы промокоды')
