from django import forms
from django.utils import timezone
from .models import Transaction, Status, TransactionType, Category, Subcategory


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Для новых записей устанавливаем сегодняшнюю дату
        if not self.instance.pk:
            today = timezone.now().date()
            self.fields['date'].initial = today
            self.fields['date'].widget.attrs['value'] = today.strftime('%Y-%m-%d')

        # Настройка выпадающих списков
        self.fields['status'].queryset = Status.objects.all()
        self.fields['transaction_type'].queryset = TransactionType.objects.all()

        if not self.instance.pk:
            self.fields['category'].queryset = Category.objects.all().order_by('name')
            self.fields['subcategory'].queryset = Subcategory.objects.all().order_by('name')
        else:
            self.fields['category'].queryset = Category.objects.filter(
                transaction_type=self.instance.transaction_type
            ).order_by('name')
            self.fields['subcategory'].queryset = Subcategory.objects.filter(
                category=self.instance.category
            ).order_by('name')

        # AJAX обработка
        if 'transaction_type' in self.data:
            try:
                transaction_type_id = int(self.data.get('transaction_type'))
                self.fields['category'].queryset = Category.objects.filter(
                    transaction_type_id=transaction_type_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(
                    category_id=category_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass

    def clean_date(self):
        """Если дата не указана, используем сегодняшнюю"""
        date = self.cleaned_data.get('date')
        if not date:
            date = timezone.now().date()
        return date


class TransactionFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата с'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата по'
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        empty_label="Все статусы",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус'
    )
    transaction_type = forms.ModelChoiceField(
        queryset=TransactionType.objects.all(),
        required=False,
        empty_label="Все типы",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип операции'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Все категории",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Категория'
    )
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        required=False,
        empty_label="Все подкатегории",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Подкатегория'
    )
