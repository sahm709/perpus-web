from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Book, Student, Visit, Borrowing
from .forms import VisitRecordForm, HistoryCheckForm, BorrowRequestForm, ReturnRequestForm  # Asumsikan ReturnRequestForm dibuat

def home(request):
    new_books = Book.objects.filter(is_available=True).order_by('-added_date')[:5]
    available_books = Book.objects.filter(is_available=True)
    return render(request, 'library/home.html', {'new_books': new_books, 'available_books': available_books})

def catalog_search(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'library/catalog.html', {'books': books, 'query': query})

def record_visit(request):
    if request.method == 'POST':
        form = VisitRecordForm(request.POST)
        if form.is_valid():
            student, created = Student.objects.get_or_create(name=form.cleaned_data['name'], grade=form.cleaned_data['grade'])
            Visit.objects.create(student=student, book_read=form.cleaned_data['book_read'])
            messages.success(request, 'Kunjungan tercatat!')
            return redirect('home')
    else:
        form = VisitRecordForm()
    return render(request, 'library/record_visit.html', {'form': form})

def history_check(request):
    visits = None
    borrowings = None
    student = None
    if request.method == 'POST':
        form = HistoryCheckForm(request.POST)
        if form.is_valid():
            try:
                student = Student.objects.get(name=form.cleaned_data['name'], grade=form.cleaned_data['grade'])
                visits = Visit.objects.filter(student=student).order_by('-visit_date')
                borrowings = Borrowing.objects.filter(student=student).order_by('-borrow_date')
            except Student.DoesNotExist:
                messages.error(request, 'Siswa tidak ditemukan.')
    else:
        form = HistoryCheckForm()
    return render(request, 'library/history_check.html', {'form': form, 'visits': visits, 'borrowings': borrowings, 'student': student})

def borrow_request(request):
    if request.method == 'POST':
        form = BorrowRequestForm(request.POST)
        if form.is_valid():
            student, created = Student.objects.get_or_create(name=form.cleaned_data['name'], grade=form.cleaned_data['grade'])
            Borrowing.objects.create(student=student, book=form.cleaned_data['book'], book_manual=form.cleaned_data['book_manual'], status='pending')
            messages.success(request, 'Pengajuan peminjaman berhasil!')
            return redirect('home')
    else:
        form = BorrowRequestForm()
    return render(request, 'library/borrow_request.html', {'form': form})

def return_request(request):
    if request.method == 'POST':
        form = ReturnRequestForm(request.POST)
        if form.is_valid():
            borrowing = Borrowing.objects.get(id=form.cleaned_data['borrowing_id'])
            borrowing.status = 'pending_return'
            borrowing.save()
            messages.success(request, 'Pengajuan pengembalian berhasil!')
            return redirect('home')
    else:
        form = ReturnRequestForm()
    return render(request, 'library/return_request.html', {'form': form})

@login_required
def admin_dashboard(request):
    pending_borrowings = Borrowing.objects.filter(status='pending').order_by('-borrow_date')
    pending_returns = Borrowing.objects.filter(status='pending_return').order_by('-borrow_date')
    return render(request, 'library/admin_dashboard.html', {'pending_borrowings': pending_borrowings, 'pending_returns': pending_returns})

@login_required
def verify_borrowing(request, borrowing_id):
    borrowing = get_object_or_404(Borrowing, id=borrowing_id, status='pending')
    if request.method == 'POST':
        borrowing.status = 'approved'
        borrowing.save()
        return redirect('admin_dashboard')
    return render(request, 'library/verify_borrowing.html', {'borrowing': borrowing})