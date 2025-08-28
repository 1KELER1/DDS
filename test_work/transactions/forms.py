from django import forms
from django.utils import timezone
from .models import Transaction, Status, TransactionType, Category, Subcategory


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'transaction_type' in self.data:
            try:
                transaction_type_id = int(self.data.get('transaction_type'))
                self.fields['category'].queryset = Category.objects.filter(transaction_type_id=transaction_type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.transaction_type.categories.all()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.all()


class TransactionFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        empty_label="Все статусы",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    transaction_type = forms.ModelChoiceField(
        queryset=TransactionType.objects.all(),
        required=False,
        empty_label="Все типы",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Все категории",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        required=False,
        empty_label="Все подкатегории",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
