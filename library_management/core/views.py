from rest_framework.viewsets import ModelViewSet # type: ignore
from .models import User, Book, Membership, Transaction, OverdueReport
from .serializers import UserSerializer, BookSerializer, MembershipSerializer, TransactionSerializer, OverdueReportSerializer
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import BookForm , UserForm , MembershipForm
from datetime import date, timedelta
from django.db.models import Count
from django.utils.timezone import now


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class MembershipViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class OverdueReportViewSet(ModelViewSet):
    queryset = OverdueReport.objects.all()
    serializer_class = OverdueReportSerializer

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            return render(request, "core/login.html", {"error": "Invalid credentials"})
    return render(request, "core/login.html")

# logout user
def user_logout(request):
    logout(request)
    return redirect("user_login")

# Admin Dashboard
@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("You do not have permission to access this page.")
    return render(request, "core/admin_dashboard.html")

# User Dashboard
@login_required
def user_dashboard(request):
    if request.user.is_admin:
        return redirect("admin_dashboard")
    return render(request, "core/user_dashboard.html")

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, "core/book_list.html", {"books": books})


@login_required
def add_book(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can add books.")
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "core/add_book.html", {"form": form})


@login_required
def update_book(request, book_id):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can update books.")
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "core/update_book.html", {"form": form, "book": book})


@login_required
def delete_book(request, book_id):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can delete books.")
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect("book_list")

@login_required
def user_list(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can view this page.")
    users = User.objects.filter(is_member=True)
    return render(request, "core/user_list.html", {"users": users})


@login_required
def user_detail(request, user_id):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can view this page.")
    user = get_object_or_404(User, id=user_id)
    membership = Membership.objects.filter(user=user).first()
    return render(request, "core/user_detail.html", {"user": user, "membership": membership})


@login_required
def add_user(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can add users.")
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserForm()
    return render(request, "core/add_user.html", {"form": form})


@login_required
def update_user(request, user_id):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can update users.")
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserForm(instance=user)
    return render(request, "core/update_user.html", {"form": form})


@login_required
def delete_user(request, user_id):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can delete users.")
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect("user_list")

from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Book
from django.contrib.auth.decorators import login_required

@login_required
def request_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.copies_available <= 0:
        return render(request, "core/book_unavailable.html")
    Transaction.objects.create(user=request.user, book=book)
    return redirect("user_dashboard")


@login_required
def admin_transactions(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")
    transactions = Transaction.objects.all()
    return render(request, "core/admin_transactions.html", {"transactions": transactions})


@login_required
def approve_request(request, transaction_id):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can approve requests.")
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.status = "APPROVED"
    transaction.book.copies_available -= 1
    transaction.book.save()
    transaction.save()
    return redirect("admin_transactions")


@login_required
def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.status = "RETURNED"
    transaction.return_date = date.today()
    overdue_days = (transaction.return_date - transaction.issue_date).days - 14  # 14-day loan period
    if overdue_days > 0:
        transaction.calculate_fine(overdue_days)
    transaction.book.copies_available += 1
    transaction.book.save()
    transaction.save()
    return redirect("user_dashboard")


@login_required
def pay_fine(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if transaction.user != request.user:
        return HttpResponseForbidden("You cannot pay fines for this transaction.")
    transaction.fine = 0  # Assume the fine is paid
    transaction.save()
    return redirect("user_dashboard")


@login_required
def overdue_books_report(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")

    overdue_transactions = []
    for transaction in Transaction.objects.filter(status="APPROVED", return_date__lt=date.today()):
        overdue_days = (date.today() - transaction.return_date).days
        overdue_transactions.append({
            "user": transaction.user,
            "book": transaction.book,
            "overdue_days": overdue_days,
            "fine": transaction.fine,
        })

    return render(request, "core/overdue_books_report.html", {"overdue_transactions": overdue_transactions})

@login_required
def active_issues_report(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")
    active_transactions = Transaction.objects.filter(status="APPROVED")
    return render(request, "core/active_issues_report.html", {"active_transactions": active_transactions})


@login_required
def user_activity_report(request, user_id):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")
    user = get_object_or_404(User, id=user_id)
    transactions = Transaction.objects.filter(user=user)
    return render(request, "core/user_activity_report.html", {"transactions": transactions, "user": user})


@login_required
def most_issued_books_chart(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")
    book_stats = (
        Transaction.objects.filter(status="APPROVED")
        .values("book__title")
        .annotate(issue_count=Count("book"))
        .order_by("-issue_count")
    )
    return render(request, "core/most_issued_books_chart.html", {"book_stats": book_stats})

@login_required
def housekeeping(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")

    # Remove expired memberships
    expired_memberships = Membership.objects.filter(end_date__lt=now())
    expired_memberships.delete()

    # Archive old transactions
    archive_date = now() - timedelta(days=365)  # Archive transactions older than 1 year
    old_transactions = Transaction.objects.filter(return_date__lt=archive_date)
    old_transactions.delete()

    return render(request, "core/maintenance-mode.html", {"expired_count": expired_memberships.count(), "archived_count": old_transactions.count()})


@login_required
def manage_memberships(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")
    memberships = Membership.objects.all()
    return render(request, "core/manage_memberships.html", {"memberships": memberships})