from django.contrib import admin
from .models import User, Book, Membership, Transaction, OverdueReport

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Membership)
admin.site.register(Transaction)
admin.site.register(OverdueReport)
