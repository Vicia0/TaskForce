from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import User, Account, Transaction, Category, Subcategory
from .forms import TransactionForm, CategoryForm, SubcategoryForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import UserRegistrationForm, CustomAuthForm

def index(request):
    return render(request, 'index.html')

def register(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'Account succesfully created. You can now login')
            return redirect('walletapp:login')
    return render(request, "register.html", context = {"form":form})

def login_user(request):
    form = CustomAuthForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email = cd['email'], password=cd['password']) 
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next','walletapp:home'))
            else:
                messages.error(request, 'Account does not exist')
    return render(request, "login.html", context = {"form":form})

@login_required
def user_transactions(request, username):
    user = get_object_or_404(User, username=username)
    the_transactions = Transaction.objects.filter(user=request.user)
    
    if not the_transactions.exists():
        the_transactions = [{
            'date': None,
            'account': None,
            'description': 'Account',
            'amount': 0,
            'transaction_type': 'None'
        }]
    
    return render(request, 'transaction.html', {'transactions': the_transactions})

@login_required
@require_POST
def create_transaction(request):
    form = TransactionForm(request.POST)
    
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()

        # Call the notification function
        send_notification(request.user, transaction)
        
        messages.success(request, 'Transaction created successfully.')
        return redirect('walletapp:user_transactions')
    
    # If form is invalid, render it with errors
    return render(request, 'transaction.html', {'form': form})

@login_required
@require_POST
def set_budget(request):
    budget = request.POST['budget']
    request.user.budget = budget
    request.user.save()

    # Update is_notify for transactions
    request.user.transactions.update(is_notify=False)
    request.user.transactions.filter(amount__gt=budget).update(is_notify=True)

    messages.success(request, 'Budget set successfully.')
    return redirect('walletapp:user_transactions')

@login_required
def report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    transactions = Transaction.objects.filter(user=request.user, date__range=(start_date, end_date))
    return render(request, 'report.html', {'transactions': transactions})

@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'categories.html', {'categories': categories})

@login_required
@require_POST
def add_category(request):
    form = CategoryForm(request.POST)

    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category.save()

        messages.success(request, 'Category added successfully.')
        return redirect('walletapp:categories')

    messages.error(request, 'Invalid form data. Please check your inputs.')
    return redirect('walletapp:categories')

@login_required
def subcategories(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    subcategories = Subcategory.objects.filter(category=category)
    return render(request, 'subcategories.html', {'subcategories': subcategories})

@login_required
@require_POST
def add_subcategory(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    form = SubcategoryForm(request.POST)

    if form.is_valid():
        subcategory = form.save(commit=False)
        subcategory.category = category
        subcategory.save()

        messages.success(request, 'Subcategory added successfully.')
        return redirect('walletapp:subcategories', category_id=category_id)

    messages.error(request, 'Invalid form data. Please check your inputs.')
    return redirect('walletapp:subcategories', category_id=category_id)

def send_notification(user, transaction):
    budget = user.budget
    amount = transaction.amount

    if amount > budget:
        message = f"Your transaction of {amount} exceeded your budget of {budget}."
        send_email(user.email, message)

def send_email(email, message):
    # Implement your email sending logic here
    pass
