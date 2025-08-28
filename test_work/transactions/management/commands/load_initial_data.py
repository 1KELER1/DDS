from django.core.management.base import BaseCommand
from transactions.models import Status, TransactionType, Category, Subcategory


class Command(BaseCommand):
    help = 'Загрузить начальные данные для справочников'

    def handle(self, *args, **options):
        # Статусы
        statuses = ['Бизнес', 'Личное', 'Налог']
        for status_name in statuses:
            status, created = Status.objects.get_or_create(name=status_name)
            if created:
                self.stdout.write(f'Создан статус: {status_name}')

        # Типы операций
        income_type, created = TransactionType.objects.get_or_create(name='Пополнение')
        if created:
            self.stdout.write('Создан тип: Пополнение')

        expense_type, created = TransactionType.objects.get_or_create(name='Списание')
        if created:
            self.stdout.write('Создан тип: Списание')

        # Категории для СПИСАНИЙ
        infra_cat, created = Category.objects.get_or_create(
            name='Инфраструктура',
            transaction_type=expense_type
        )
        if created:
            self.stdout.write('Создана категория: Инфраструктура (Списание)')

        marketing_cat, created = Category.objects.get_or_create(
            name='Маркетинг',
            transaction_type=expense_type
        )
        if created:
            self.stdout.write('Создана категория: Маркетинг (Списание)')

        # Категории для ПОПОЛНЕНИЙ
        salary_cat, created = Category.objects.get_or_create(
            name='Зарплата',
            transaction_type=income_type
        )
        if created:
            self.stdout.write('Создана категория: Зарплата (Пополнение)')

        business_income_cat, created = Category.objects.get_or_create(
            name='Доходы от бизнеса',
            transaction_type=income_type
        )
        if created:
            self.stdout.write('Создана категория: Доходы от бизнеса (Пополнение)')

        # Подкатегории для Инфраструктуры (Списание)
        vps_subcat, created = Subcategory.objects.get_or_create(name='VPS', category=infra_cat)
        if created:
            self.stdout.write('Создана подкатегория: VPS')

        proxy_subcat, created = Subcategory.objects.get_or_create(name='Proxy', category=infra_cat)
        if created:
            self.stdout.write('Создана подкатегория: Proxy')

        # Подкатегории для Маркетинга (Списание)
        farpost_subcat, created = Subcategory.objects.get_or_create(name='Farpost', category=marketing_cat)
        if created:
            self.stdout.write('Создана подкатегория: Farpost')

        avito_subcat, created = Subcategory.objects.get_or_create(name='Avito', category=marketing_cat)
        if created:
            self.stdout.write('Создана подкатегория: Avito')

        # Подкатегории для Зарплаты (Пополнение)
        main_job_subcat, created = Subcategory.objects.get_or_create(name='Основная работа', category=salary_cat)
        if created:
            self.stdout.write('Создана подкатегория: Основная работа')

        part_time_subcat, created = Subcategory.objects.get_or_create(name='Подработка', category=salary_cat)
        if created:
            self.stdout.write('Создана подкатегория: Подработка')

        # Подкатегории для Доходов от бизнеса (Пополнение)
        sales_subcat, created = Subcategory.objects.get_or_create(name='Продажи', category=business_income_cat)
        if created:
            self.stdout.write('Создана подкатегория: Продажи')

        services_subcat, created = Subcategory.objects.get_or_create(name='Услуги', category=business_income_cat)
        if created:
            self.stdout.write('Создана подкатегория: Услуги')

        self.stdout.write(self.style.SUCCESS('Загрузка начальных данных завершена'))
