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
from django.db.models import Q
from django.utils.timezone import now
from django.contrib import messages

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
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect("admin_dashboard")
            return redirect("user_dashboard")
        else:
            error = "Invalid username or password"
    return render(request, "core/login.html", {
        "error": error,
        "allow_registration": True,
        "allow_password_reset": True,
    })

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
    search_query = request.GET.get("search", "")
    books = Book.objects.all()

    # Filter books by title or author
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )

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
        return render(request, "core/book_unavailable.html", {"book": book})

    # Create a new transaction with status "REQUESTED"
    Transaction.objects.create(user=request.user, book=book, status="REQUESTED", issue_date=None)

    # Provide feedback and redirect
    messages.success(request, f'Your request for "{book.title}" has been placed successfully.')
    return redirect("user_dashboard")


@login_required
def admin_transactions(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")
    
    # Fetch query parameters
    search_query = request.GET.get("search", "")
    selected_status = request.GET.get("status", "all")

    # Base queryset
    transactions = Transaction.objects.all()

    # Filter by search
    if search_query:
        transactions = transactions.filter(
            Q(user__username__icontains=search_query) |
            Q(book__title__icontains=search_query)
        )

    # Filter by status
    if selected_status != "all":
        transactions = transactions.filter(status=selected_status)

    return render(request, "core/admin_transactions.html", {
        "transactions": transactions,
        "selected_status": selected_status
    })


@login_required
def approve_request(request, transaction_id):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can approve requests.")
    
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if transaction.status != "REQUESTED":
        messages.error(request, "This transaction is no longer pending approval.")
        return redirect("admin_transactions")

    if transaction.book.copies_available <= 0:
        messages.error(request, f'The book "{transaction.book.title}" is no longer available.')
        return redirect("admin_transactions")

    transaction.status = "APPROVED"
    transaction.issue_date = date.today()  # Set issue_date when approving
    transaction.book.copies_available -= 1
    transaction.book.save()
    transaction.save()

    messages.success(request, f'The request for "{transaction.book.title}" has been approved successfully.')
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



def overdue_books_report(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")

    overdue_transactions = []
    for transaction in Transaction.objects.filter(status="APPROVED", return_date__lt=date.today()):
        overdue_days = (date.today() - transaction.return_date).days
        fine = overdue_days * 10  # Example fine: $10 per overdue day
        overdue_transactions.append({
            "user": transaction.user,
            "book": transaction.book,
            "overdue_days": overdue_days,
            "fine": fine,
        })

    return render(request, "core/overdue_books_report.html", {"overdue_transactions": overdue_transactions})


@login_required
def active_issues_report(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")
    
    search_query = request.GET.get("search", "")
    active_transactions = Transaction.objects.filter(status="APPROVED")

    if search_query:
        active_transactions = active_transactions.filter(
            Q(user__username__icontains=search_query) |
            Q(book__title__icontains=search_query)
        )
    
    return render(request, "core/active_issues_report.html", {"active_transactions": active_transactions})


@login_required
def user_activity_report(request, user_id=None):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")
    
    users = User.objects.all()
    selected_user = None
    transactions = None

    if user_id:
        selected_user = get_object_or_404(User, id=user_id)
        transactions = Transaction.objects.filter(user=selected_user).order_by("-issue_date")
    
    return render(request, "core/user_activity_report.html", {
        "users": users,
        "selected_user": selected_user,
        "transactions": transactions,
    })

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
    
    search_query = request.GET.get("search", "")
    memberships = Membership.objects.all()

    # Filter memberships by username or membership type
    if search_query:
        memberships = memberships.filter(
            Q(user__username__icontains=search_query) |
            Q(membership_type__icontains=search_query)
        )

    return render(request, "core/manage_memberships.html", {"memberships": memberships})

@login_required
def add_membership(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("Only admins can access this page.")
    
    if request.method == "POST":
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_memberships")
    else:
        form = MembershipForm()
    
    return render(request, "core/add_membership.html", {"form": form})

@login_required
def my_issued_books(request):
    # Filter transactions for the logged-in user with approved status
    transactions = Transaction.objects.filter(user=request.user, status="APPROVED").order_by("-issue_date")
    return render(request, "core/my_issued_books.html", {"transactions": transactions})
   
def pay_fines(request):
    # Retrieve all transactions with unpaid fines for the logged-in user
    transactions_with_fines = Transaction.objects.filter(user=request.user, fine__gt=0)
    
    total_fine = sum(transaction.fine for transaction in transactions_with_fines)

    if request.method == "POST":
        # Simulate payment logic: Clear fines for all unpaid transactions
        for transaction in transactions_with_fines:
            transaction.fine = 0
            transaction.save()
        return render(request, "core/fines_paid.html")

    return render(request, "core/pay_fines.html", {
        "transactions_with_fines": transactions_with_fines,
        "total_fine": total_fine,
    })