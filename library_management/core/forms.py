from django import forms
from .models import Book , User, Membership

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "is_member", "is_admin"]

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ["membership_type", "start_date", "end_date", "user"]

class MembershipManagementForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ["user", "membership_type", "start_date", "end_date"]