from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User Model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)


# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    copies_available = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# Membership Model
class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.membership_type}"


# Transaction Model
class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=[("REQUESTED", "Requested"), ("APPROVED", "Approved"), ("RETURNED", "Returned")],
        default="REQUESTED",
    )
    def calculate_fine(self, overdue_days):
        self.fine = overdue_days * 10  # Example fine: $10/day
        self.save()
        
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


# Overdue Report
class OverdueReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    days_overdue = models.IntegerField()
    fine = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.days_overdue} days"
