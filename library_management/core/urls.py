from django.urls import path, include
from rest_framework.routers import DefaultRouter # type: ignore
from . import views

# API Router
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'memberships', views.MembershipViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'overdues', views.OverdueReportViewSet)

# Frontend URL patterns
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.add_book, name="add_book"),
    path("books/update/<int:book_id>/", views.update_book, name="update_book"),
    path("books/delete/<int:book_id>/", views.delete_book, name="delete_book"),
    path("users/", views.user_list, name="user_list"),
    path("users/<int:user_id>/", views.user_detail, name="user_detail"),
    path("users/add/", views.add_user, name="add_user"),
    path("users/update/<int:user_id>/", views.update_user, name="update_user"),
    path("users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("transactions/admin/", views.admin_transactions, name="admin_transactions"),
    path("transactions/request/<int:book_id>/", views.request_book, name="request_book"),
    path("transactions/approve/<int:transaction_id>/", views.approve_request, name="approve_request"),
    path("transactions/return/<int:transaction_id>/", views.return_book, name="return_book"),
    path("transactions/pay-fine/<int:transaction_id>/", views.pay_fine, name="pay_fine"),
    path("reports/overdue-books/", views.overdue_books_report, name="overdue_books_report"),
    path("reports/active-issues/", views.active_issues_report, name="active_issues_report"),
    path("reports/user-activity/<int:user_id>/", views.user_activity_report, name="user_activity_report"),
    path("reports/most-issued-books/", views.most_issued_books_chart, name="most_issued_books_chart"),
    path("maintenance/mode/", views.housekeeping, name="housekeeping"),
    path("maintenance/memberships/", views.manage_memberships, name="manage_memberships"),

]


# Add API routes separately
'''urlpatterns += [
    path("api/", include(router.urls)),  # All API routes under /api/
]'''
