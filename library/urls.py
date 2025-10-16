from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog_search, name='catalog_search'),
    path('visit/', views.record_visit, name='record_visit'),
    path('history/', views.history_check, name='history_check'),
    path('borrow/', views.borrow_request, name='borrow_request'),
    path('return/', views.return_request, name='return_request'),
    path('admin-panel/dashboard/', login_required(views.admin_dashboard), name='admin_dashboard'),
    path('admin-panel/verify/<int:borrowing_id>/', login_required(views.verify_borrowing), name='verify_borrowing'),
]