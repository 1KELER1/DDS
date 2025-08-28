from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Статус")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Тип операции")

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name="Тип операции"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ('name', 'transaction_type')

    def __str__(self):
        return f"{self.name} ({self.transaction_type.name})"


class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Подкатегория")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Transaction(models.Model):
    date = models.DateField(verbose_name="Дата")
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        verbose_name="Статус"
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        verbose_name="Тип операции"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Сумма"
    )
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.amount} руб. ({self.transaction_type.name})"
