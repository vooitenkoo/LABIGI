from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def get_default_end_date():
    return timezone.now() + timezone.timedelta(days=30)

def validate_driver_age(birth_date):
    if birth_date:
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise ValidationError('Водитель должен быть старше 18 лет.')

class VehicleType(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', default='')

    class Meta:
        verbose_name = 'Тип транспорта'
        verbose_name_plural = 'Типы транспорта'

    def __str__(self):
        return self.name

class BodyType(models.Model):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Тип кузова'
        verbose_name_plural = 'Типы кузовов'

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    type = models.ForeignKey(VehicleType, on_delete=models.PROTECT, verbose_name='Тип')
    body_type = models.ForeignKey(BodyType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип кузова')
    brand = models.CharField('Марка', max_length=200, default='Не указано')
    model = models.CharField('Модель', max_length=200, default='Не указано')
    year = models.PositiveIntegerField('Год выпуска', default=2024)
    plate_number = models.CharField('Гос. номер', max_length=20, default='Не указано')
    capacity = models.DecimalField('Грузоподъемность (кг)', max_digits=10, decimal_places=2, default=1000.00)
    is_available = models.BooleanField('Доступен', default=True)
    image = models.ImageField('Изображение', upload_to='vehicles/', null=True, blank=True)

    class Meta:
        verbose_name = 'Транспортное средство'
        verbose_name_plural = 'Транспортные средства'

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Телефон', max_length=20, default='+375')
    experience = models.PositiveIntegerField('Опыт (лет)', default=0)
    categories = models.CharField('Категории прав', max_length=50, default='B')
    vehicle = models.ForeignKey('Vehicle', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Транспортное средство')
    photo = models.ImageField('Фото', upload_to='drivers/', null=True, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    def get_age(self):
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return self.user.get_full_name()

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Телефон', max_length=20, default='+375')
    address = models.CharField('Адрес', max_length=500, default='')
    company_name = models.CharField('Название компании', max_length=200, blank=True, default='')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.user.get_full_name()

class CargoType(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', default='')
    special_requirements = models.TextField('Особые требования', blank=True, default='')

    class Meta:
        verbose_name = 'Тип груза'
        verbose_name_plural = 'Типы грузов'

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', default='')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT, verbose_name='Тип транспорта')
    base_price = models.DecimalField('Базовая цена', max_digits=10, decimal_places=2, default=0.00)
    max_weight = models.DecimalField('Максимальный вес (кг)', max_digits=10, decimal_places=2, default=1000.00)
    max_volume = models.DecimalField('Максимальный объем (м³)', max_digits=10, decimal_places=2, default=10.00)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name

class Schedule(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['driver', 'date', 'start_time']

    def __str__(self):
        return f"{self.driver} - {self.date} ({self.start_time}-{self.end_time})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('accepted', 'Принят'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен')
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    cargo_type = models.ForeignKey(CargoType, on_delete=models.CASCADE)
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    weight = models.FloatField(validators=[MinValueValidator(0.1)])
    volume = models.FloatField(validators=[MinValueValidator(0.1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Заказ #{self.id} - {self.client}"

    class Meta:
        ordering = ['-created_at']

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField('Текст отзыва')
    rating = models.IntegerField('Оценка', choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Отзыв от {self.user.username} ({self.rating}/5)'

class Promotion(models.Model):
    code = models.CharField('Промокод', max_length=20, unique=True)
    description = models.TextField('Описание', default='')
    discount_percent = models.DecimalField('Процент скидки', max_digits=5, decimal_places=2, default=0.00)
    start_date = models.DateTimeField('Дата начала', default=timezone.now)
    end_date = models.DateTimeField('Дата окончания', default=get_default_end_date)
    is_active = models.BooleanField('Активна', default=True)
    max_uses = models.PositiveIntegerField('Макс. использований', null=True, blank=True, default=100)
    used_count = models.PositiveIntegerField('Использовано раз', default=0)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    short_content = models.CharField('Краткое содержание', max_length=500, default='')
    image = models.ImageField('Изображение', upload_to='news/', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Partner(models.Model):
    name = models.CharField('Название компании', max_length=200)
    description = models.TextField('Описание', blank=True)
    logo = models.ImageField('Логотип', upload_to='partners/', null=True, blank=True)
    website_url = models.URLField('Ссылка на сайт', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Название товара/услуги', max_length=200)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/', null=True, blank=True)
    category = models.CharField('Категория', max_length=100, default='Услуга')
    is_available = models.BooleanField('Доступен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары/Услуги'
        ordering = ['name']

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество', default=1)
    added_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['user', 'product']

    def __str__(self):
        return f'{self.user.username} - {self.product.name} x{self.quantity}'

    @property
    def total_price(self):
        return self.product.price * self.quantity

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('failed', 'Ошибка оплаты'),
        ('refunded', 'Возвращен')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField('Способ оплаты', max_length=50, default='card')
    transaction_id = models.CharField('ID транзакции', max_length=100, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    paid_at = models.DateTimeField('Дата оплаты', null=True, blank=True)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']

    def __str__(self):
        return f'Платеж #{self.id} - {self.user.username}'

class CompanyInfo(models.Model):
    name = models.CharField('Название компании', max_length=200)
    description = models.TextField('Описание компании')
    logo = models.ImageField('Логотип', upload_to='company/', null=True, blank=True)
    video_url = models.URLField('Ссылка на видео', blank=True)
    video_file = models.FileField('Видео файл', upload_to='company/videos/', blank=True, null=True)
    history = models.TextField('История компании', blank=True)
    requisites = models.TextField('Реквизиты', blank=True)
    certificate_text = models.TextField('Текст сертификата', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'

    def __str__(self):
        return self.name

class CompanyHistory(models.Model):
    year = models.PositiveIntegerField('Год')
    event = models.TextField('Событие')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'История компании'
        verbose_name_plural = 'История компании'
        ordering = ['year']

    def __str__(self):
        return f'{self.year}: {self.event[:50]}...'

class Dictionary(models.Model):
    term = models.CharField('Термин', max_length=200)
    definition = models.TextField('Определение')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Словарь'
        verbose_name_plural = 'Словарь терминов'
        ordering = ['term']

    def __str__(self):
        return self.term

class FAQ(models.Model):
    question = models.CharField('Вопрос', max_length=500)
    answer = models.TextField('Ответ')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'Часто задаваемые вопросы'
        ordering = ['created_at']

    def __str__(self):
        return self.question

class Employee(models.Model):
    name = models.CharField('Имя', max_length=100)
    position = models.CharField('Должность', max_length=100)
    description = models.TextField('Описание работы')
    phone = models.CharField('Телефон', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    photo = models.ImageField('Фото', upload_to='employees/', null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.position}'

class Vacancy(models.Model):
    title = models.CharField('Название вакансии', max_length=200)
    description = models.TextField('Описание')
    requirements = models.TextField('Требования', blank=True)
    salary = models.CharField('Зарплата', max_length=100, blank=True)
    location = models.CharField('Местоположение', max_length=100, default='Минск')
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class PromoCode(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('archived', 'В архиве'),
        ('expired', 'Истек')
    ]
    
    code = models.CharField('Промокод', max_length=20, unique=True)
    description = models.TextField('Описание')
    discount_percent = models.DecimalField('Процент скидки', max_digits=5, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField('Сумма скидки', max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateTimeField('Дата начала', default=timezone.now)
    end_date = models.DateTimeField('Дата окончания', default=get_default_end_date)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='active')
    max_uses = models.PositiveIntegerField('Макс. использований', null=True, blank=True, default=100)
    used_count = models.PositiveIntegerField('Использовано раз', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

    def is_valid(self):
        now = timezone.now()
        return (self.status == 'active' and 
                self.start_date <= now <= self.end_date and
                (self.max_uses is None or self.used_count < self.max_uses))

class Banner(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='banners/')
    link_url = models.URLField('Ссылка', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
