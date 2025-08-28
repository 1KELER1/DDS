from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Transaction, Status, TransactionType, Category, Subcategory
from .forms import TransactionForm, TransactionFilterForm


def transaction_list(request):
    transactions = Transaction.objects.select_related(
        'status', 'transaction_type', 'category', 'subcategory'
    ).all()

    filter_form = TransactionFilterForm(request.GET)

    if filter_form.is_valid():
        if filter_form.cleaned_data['date_from']:
            transactions = transactions.filter(date__gte=filter_form.cleaned_data['date_from'])
        if filter_form.cleaned_data['date_to']:
            transactions = transactions.filter(date__lte=filter_form.cleaned_data['date_to'])
        if filter_form.cleaned_data['status']:
            transactions = transactions.filter(status=filter_form.cleaned_data['status'])
        if filter_form.cleaned_data['transaction_type']:
            transactions = transactions.filter(transaction_type=filter_form.cleaned_data['transaction_type'])
        if filter_form.cleaned_data['category']:
            transactions = transactions.filter(category=filter_form.cleaned_data['category'])
        if filter_form.cleaned_data['subcategory']:
            transactions = transactions.filter(subcategory=filter_form.cleaned_data['subcategory'])

    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
    }
    return render(request, 'transactions/transaction_list.html', context)


def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)

        # Если дата не передана в POST, добавляем сегодняшнюю дату
        data = request.POST.copy()
        if not data.get('date'):
            data['date'] = timezone.now().date().strftime('%Y-%m-%d')

        form = TransactionForm(data)

        if form.is_valid():
            transaction = form.save(commit=False)
            # Убеждаемся, что дата установлена
            if not transaction.date:
                transaction.date = timezone.now().date()
            transaction.save()
            messages.success(request, 'Запись успешно создана!')
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    return render(request, 'transactions/transaction_form.html', {'form': form, 'title': 'Создать запись'})


def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'transactions/transaction_form.html', {'form': form, 'title': 'Редактировать запись'})


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Запись успешно удалена!')
        return redirect('transaction_list')

    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})


def load_categories(request):
    transaction_type_id = request.GET.get('transaction_type')
    categories = Category.objects.filter(transaction_type_id=transaction_type_id).order_by('name')
    return JsonResponse(list(categories.values('id', 'name')), safe=False)


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)


def dictionaries(request):
    context = {
        'statuses': Status.objects.all(),
        'transaction_types': TransactionType.objects.all(),
        'categories': Category.objects.select_related('transaction_type').all(),
        'subcategories': Subcategory.objects.select_related('category').all(),
    }
    return render(request, 'transactions/dictionaries.html', context)


# Управление статусами
def add_status(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Status.objects.create(name=name)
            messages.success(request, f'Статус "{name}" успешно добавлен!')
    return redirect('dictionaries')


def edit_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            status.name = name
            status.save()
            messages.success(request, f'Статус "{name}" успешно обновлен!')
    return redirect('dictionaries')


def delete_status(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        name = status.name
        try:
            status.delete()
            messages.success(request, f'Статус "{name}" успешно удален!')
        except Exception as e:
            messages.error(request, f'Невозможно удалить статус "{name}". Он используется в транзакциях.')
    return redirect('dictionaries')


# Управление типами операций
def add_transaction_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            TransactionType.objects.create(name=name)
            messages.success(request, f'Тип операции "{name}" успешно добавлен!')
    return redirect('dictionaries')


def edit_transaction_type(request, pk):
    transaction_type = get_object_or_404(TransactionType, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            transaction_type.name = name
            transaction_type.save()
            messages.success(request, f'Тип операции "{name}" успешно обновлен!')
    return redirect('dictionaries')


def delete_transaction_type(request, pk):
    transaction_type = get_object_or_404(TransactionType, pk=pk)
    if request.method == 'POST':
        name = transaction_type.name
        try:
            transaction_type.delete()
            messages.success(request, f'Тип операции "{name}" успешно удален!')
        except Exception as e:
            messages.error(request, f'Невозможно удалить тип операции "{name}". Он используется в транзакциях.')
    return redirect('dictionaries')


# Управление категориями
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        transaction_type_id = request.POST.get('transaction_type')
        if name and transaction_type_id:
            transaction_type = get_object_or_404(TransactionType, pk=transaction_type_id)
            Category.objects.create(name=name, transaction_type=transaction_type)
            messages.success(request, f'Категория "{name}" успешно добавлена!')
    return redirect('dictionaries')


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        transaction_type_id = request.POST.get('transaction_type')
        if name and transaction_type_id:
            transaction_type = get_object_or_404(TransactionType, pk=transaction_type_id)
            category.name = name
            category.transaction_type = transaction_type
            category.save()
            messages.success(request, f'Категория "{name}" успешно обновлена!')
    return redirect('dictionaries')


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        try:
            category.delete()
            messages.success(request, f'Категория "{name}" успешно удалена!')
        except Exception as e:
            messages.error(request, f'Невозможно удалить категорию "{name}". Она используется в транзакциях.')
    return redirect('dictionaries')


# Управление подкатегориями
def add_subcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            category = get_object_or_404(Category, pk=category_id)
            Subcategory.objects.create(name=name, category=category)
            messages.success(request, f'Подкатегория "{name}" успешно добавлена!')
    return redirect('dictionaries')


def edit_subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            category = get_object_or_404(Category, pk=category_id)
            subcategory.name = name
            subcategory.category = category
            subcategory.save()
            messages.success(request, f'Подкатегория "{name}" успешно обновлена!')
    return redirect('dictionaries')


def delete_subcategory(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        name = subcategory.name
        try:
            subcategory.delete()
            messages.success(request, f'Подкатегория "{name}" успешно удалена!')
        except Exception as e:
            messages.error(request, f'Невозможно удалить подкатегорию "{name}". Она используется в транзакциях.')
    return redirect('dictionaries')
