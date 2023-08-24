from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from mptt.utils import tree_item_iterator

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('bank', 'Bank'),
        ('mobile_money', 'Mobile Money'),
        ('cash', 'Cash'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=ACCOUNT_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Balance = models.IntegerField()

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return self.name

CATEGORY_TYPES = [
    ('Fashion', (
        ('Clothes', 'Clothes'),
        ('Shoes', 'Shoes')
    )),
    ('Accommodation', (
            ('Rent', 'rent'),
            ('Hotel', 'hotel')
    )),
    ('Utilities', (
        ('Electricity', 'electricity'),
        ('Water', 'water')
    )),
    ('Other', ())
]
    
class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

def extract_category_choices():
    choices = []
    for category, subcategories in CATEGORY_TYPES:
        category_choices = [(subcategory[1], subcategory[0]) for subcategory in subcategories]
        choices.append((category, category_choices))
    return choices

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPES)
    
    category = models.CharField(max_length=255, choices=extract_category_choices())
    subcategory = models.CharField(max_length=255, choices=extract_category_choices()) 
    
    date = models.DateTimeField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    is_notify = models.BooleanField(default=False)

    def __str__(self):
        return f"Transaction by {self.user.username} on {self.date}"
