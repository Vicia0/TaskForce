from django.urls import path
from .views import index, login_user, register,logout_user, userTransactions, add_account, add_transaction,report

app_name = "walletapp"
urlpatterns = [
    path('', index, name='index'),
    path('register', register, name='register'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('transactions', userTransactions, name='user_transactions'),
    path('add_account', add_account, name='add_account'),
    path('transactions/createtransaction', add_transaction, name='create_transaction'),
    path('report/', report, name='report'),
]
