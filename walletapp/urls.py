from django.urls import path
from .views import index, login_user, register, user_transactions, report, categories, subcategories
app_name = "walletapp"
urlpatterns = [
    path('', index, name='index'),
    path('login', login_user, name='login_user'),
    path('register', register, name='register'),
    path('<str:username>/transactions', user_transactions, name='user_transactions'),
    path('report', report, name='report'),
    path('categories', categories, name='categories'),
    path('categories/<int:category_id>/subcategories/', subcategories, name='subcategories'),
]