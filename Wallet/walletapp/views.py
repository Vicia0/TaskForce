from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from .forms import SignUpForm, AddAccountForm
from .models import Transaction, Account

from decimal import Decimal
from .forms import AddTransactionForm

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('walletapp:login')
    else:
        form = SignUpForm()
    return render(request, 'auth/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('walletapp:user_transactions')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', context={'form': form})

@login_required
def userTransactions(request):
    user_accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'user_pages/transactions.html', {'transactions': transactions, 'user_accounts': user_accounts})

@login_required
def logout_user(request):
    logout(request)
    return redirect('walletapp:index')

@login_required
def add_account(request):
    if request.method == 'POST':
        form = AddAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account added successfully!')
            return redirect('walletapp:user_transactions')
    else:
        form = AddAccountForm()
    return render(request, 'user_pages/add_account.html', {'form': form})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            account = transaction.account

            if transaction.transaction_type == 'expense':
                account.Balance -= transaction.amount
            elif transaction.transaction_type == 'income':
                account.Balance += transaction.amount

            account.save()
            transaction.user = request.user
            transaction.save()

            messages.success(request, 'Transaction added successfully!')
            return redirect('walletapp:user_transactions')
    else:
        form = AddTransactionForm()
        # Set default values for category and subcategory fields
        transaction_type = request.GET.get('transaction_type', '').lower()
        if transaction_type == 'expense':
            form.fields['category'].initial = 'N/A'
            form.fields['subcategory'].initial = 'N/A'
    
    context = {'form': form}
    return render(request, 'user_pages/create_transaction.html', context)

def generate_graphs(user):
    transactions = Transaction.objects.filter(user=user).order_by('date')
    balance_changes = []

    balance = 0
    for transaction in transactions:
        if transaction.transaction_type == 'expense':
            balance -= transaction.amount
        elif transaction.transaction_type == 'income':
            balance += transaction.amount
        balance_changes.append(balance)

    dates = [transaction.date for transaction in transactions]
    types = [transaction.transaction_type for transaction in transactions]
    budgets = [transaction.budget for transaction in transactions]
    amounts = [transaction.amount for transaction in transactions]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.plot(dates, budgets, label='Budget')
    ax1.plot(dates, amounts, label='Amount')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Amount')
    ax1.legend()

    ax2.plot(dates, balance_changes, label='Balance')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Balance')
    ax2.legend()

    # Convert the plot to an image and encode it
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_encoded = base64.b64encode(img_buffer.read()).decode('utf-8')

    plt.close()

    return img_encoded

def report(request):
    user = request.user
    graph_image = generate_graphs(user)
    return render(request, 'user_pages/report.html', {'graph_image': graph_image})
