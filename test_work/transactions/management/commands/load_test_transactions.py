from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from transactions.models import Transaction, Status, TransactionType, Category, Subcategory
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Загрузить тестовые записи транзакций'

    def handle(self, *args, **options):
        # Проверяем наличие справочников
        statuses = list(Status.objects.all())
        transaction_types = list(TransactionType.objects.all())

        if not (statuses and transaction_types):
            self.stdout.write(self.style.ERROR('Не найдены справочники. Сначала выполните load_initial_data'))
            return

        # Получаем типы операций
        try:
            income_type = TransactionType.objects.get(name='Пополнение')
            expense_type = TransactionType.objects.get(name='Списание')
        except TransactionType.DoesNotExist:
            self.stdout.write(self.style.ERROR('Не найдены типы операций "Пополнение" и "Списание"'))
            return

        # Получаем категории и подкатегории
        income_categories = list(Category.objects.filter(transaction_type=income_type))
        expense_categories = list(Category.objects.filter(transaction_type=expense_type))

        if not (income_categories and expense_categories):
            self.stdout.write(self.style.ERROR('Не найдены категории. Сначала выполните load_initial_data'))
            return

        # Заготовленные данные для более реалистичных записей
        test_data = [
            # Пополнения
            {
                'type': income_type,
                'amount_range': (15000, 80000),
                'comments': ['Зарплата за месяц', 'Аванс', 'Премия', 'Оплата за проект', 'Фриланс']
            },
            # Списания
            {
                'type': expense_type,
                'amount_range': (500, 15000),
                'comments': ['Оплата VPS сервера', 'Продвижение на Авито', 'Покупка прокси', 'Реклама в Farpost',
                             'Техническое обслуживание']
            }
        ]

        created_count = 0
        today = timezone.now().date()

        # Создаем 10 тестовых записей
        for i in range(10):
            # Выбираем случайный тип операции
            data_config = random.choice(test_data)
            transaction_type = data_config['type']

            # Получаем категории для выбранного типа
            if transaction_type == income_type:
                available_categories = income_categories
            else:
                available_categories = expense_categories

            if not available_categories:
                continue

            category = random.choice(available_categories)

            # Получаем подкатегории для выбранной категории
            subcategories = list(Subcategory.objects.filter(category=category))
            if not subcategories:
                continue

            subcategory = random.choice(subcategories)

            # Генерируем случайную сумму в зависимости от типа операции
            min_amount, max_amount = data_config['amount_range']
            amount = Decimal(random.randint(min_amount, max_amount))

            # Генерируем случайную дату (от сегодня до 30 дней назад)
            days_ago = random.randint(0, 30)
            transaction_date = today - timedelta(days=days_ago)

            # Выбираем случайный статус и комментарий
            status = random.choice(statuses)
            comment = random.choice(data_config['comments'])

            # Создаем транзакцию
            transaction = Transaction.objects.create(
                date=transaction_date,
                status=status,
                transaction_type=transaction_type,
                category=category,
                subcategory=subcategory,
                amount=amount,
                comment=comment
            )

            created_count += 1
            self.stdout.write(
                f'Создана транзакция {created_count}: {transaction_date} - {amount} руб. ({transaction_type.name})')

        self.stdout.write(self.style.SUCCESS(f'Загружено {created_count} тестовых записей транзакций'))

        # Показываем статистику
        total_transactions = Transaction.objects.count()
        income_total = Transaction.objects.filter(transaction_type__name='Пополнение').count()
        expense_total = Transaction.objects.filter(transaction_type__name='Списание').count()

        self.stdout.write(f'Всего транзакций в базе: {total_transactions}')
        self.stdout.write(f'Пополнений: {income_total}, Списаний: {expense_total}')
