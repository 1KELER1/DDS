from django.contrib import admin
from .models import Status, TransactionType, Category, Subcategory, Transaction


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'transaction_type']
    list_filter = ['transaction_type']
    search_fields = ['name']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'get_transaction_type']
    list_filter = ['category__transaction_type', 'category']
    search_fields = ['name']

    def get_transaction_type(self, obj):
        return obj.category.transaction_type.name

    get_transaction_type.short_description = 'Тип операции'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'transaction_type', 'category', 'subcategory', 'amount', 'status']
    list_filter = ['date', 'status', 'transaction_type', 'category']
    search_fields = ['comment']
    date_hierarchy = 'date'
