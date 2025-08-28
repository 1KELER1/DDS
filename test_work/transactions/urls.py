from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('<int:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path('<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    path('dictionaries/', views.dictionaries, name='dictionaries'),

    # URL для управления статусами
    path('status/add/', views.add_status, name='add_status'),
    path('status/<int:pk>/edit/', views.edit_status, name='edit_status'),
    path('status/<int:pk>/delete/', views.delete_status, name='delete_status'),

    # URL для управления типами операций
    path('type/add/', views.add_transaction_type, name='add_transaction_type'),
    path('type/<int:pk>/edit/', views.edit_transaction_type, name='edit_transaction_type'),
    path('type/<int:pk>/delete/', views.delete_transaction_type, name='delete_transaction_type'),

    # URL для управления категориями
    path('category/add/', views.add_category, name='add_category'),
    path('category/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),

    # URL для управления подкатегориями
    path('subcategory/add/', views.add_subcategory, name='add_subcategory'),
    path('subcategory/<int:pk>/edit/', views.edit_subcategory, name='edit_subcategory'),
    path('subcategory/<int:pk>/delete/', views.delete_subcategory, name='delete_subcategory'),
]
