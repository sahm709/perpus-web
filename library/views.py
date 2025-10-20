from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest 
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Book, Student, Visit, Borrowing, BookRequest
from .forms import VisitRecordForm, HistoryCheckForm, BorrowRequestForm, ReturnRequestForm, BookRequestForm  

def home(request):
    new_books = Book.objects.filter(is_available=True).order_by('-added_date')[:5]
    available_books = Book.objects.filter(is_available=True).order_by('-is_recommended', 'title')
    return render(request, 'library/home.html', {'new_books': new_books, 'available_books': available_books})

def catalog_search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter()  # Opsional: Hanya tampilkan buku yang tersedia (sesuai dengan home view)
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    
    books = books.order_by('-is_recommended', 'title')
    
    return render(request, 'library/catalog.html', {'books': books, 'query': query})


def record_visit(request):
    if request.method == 'POST':
        # Clean POST data sebelum masuk ke form
        post_data = request.POST.copy()
        book_value = post_data.get('book', '').strip()
        
        # Jika book bukan angka (ID), set ke kosong
        if not book_value.isdigit():
            post_data['book'] = ''
        
        form = VisitRecordForm(post_data)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            grade = form.cleaned_data['grade']
            book = form.cleaned_data.get('book')
            book_read_manual = form.cleaned_data.get('book_read_manual', '').strip()
            
            student, created = Student.objects.get_or_create(
                name=name, 
                defaults={'grade': grade}
            )
            
            if not created and student.grade != grade:
                student.grade = grade
                student.save()
            
            visit = Visit.objects.create(
                student=student,
                book=book,
                book_read_manual=book_read_manual
            )
            
            book_title = visit.book.title if visit.book else visit.book_read_manual
            messages.success(request, f'Kunjungan untuk {name} berhasil dicatat! Buku: {book_title}')
            return redirect('home')
        else:
            messages.error(request, 'Mohon isi form dengan benar.')
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
            name = form.cleaned_data['name']
            grade = form.cleaned_data['grade']
            book = form.cleaned_data.get('book')
            book_manual = form.cleaned_data.get('book_manual')
            
            try:
                student = Student.objects.get(name=name, grade=grade)
                if book:
                    borrowing = Borrowing.objects.filter(student=student, book=book, status='approved').first()
                elif book_manual:
                    borrowing = Borrowing.objects.filter(student=student, book_manual=book_manual, status='approved').first()
                else:
                    messages.error(request, 'Buku tidak ditemukan.')
                    return render(request, 'library/return_request.html', {'form': form})  # Pastikan return di sini
                
                if borrowing:
                    borrowing.status = 'pending_return'
                    borrowing.save()
                    messages.success(request, 'Pengajuan pengembalian berhasil!')
                    return redirect('home')
                else:
                    messages.error(request, 'Tidak ada peminjaman yang sesuai.')
                    return render(request, 'library/return_request.html', {'form': form})  # Pastikan return di sini
            except Student.DoesNotExist:
                messages.error(request, 'Siswa tidak ditemukan.')
                return render(request, 'library/return_request.html', {'form': form})  # Pastikan return di sini
        else:
            messages.error(request, 'Form tidak valid.')
            return render(request, 'library/return_request.html', {'form': form})  # Pastikan return di sini
    else:  # Untuk GET request
        form = ReturnRequestForm()
        return render(request, 'library/return_request.html', {'form': form})  # Pastikan return di sini

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

@login_required
def verify_return(request, borrowing_id):
    try:
        borrowing = Borrowing.objects.get(id=borrowing_id, status='pending_return')
    except Borrowing.DoesNotExist:
        messages.error(request, 'Borrowing dengan ID tersebut tidak ditemukan atau statusnya bukan pending return.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        borrowing.status = 'returned'
        borrowing.return_date = timezone.now()
        borrowing.save()
        messages.success(request, 'Pengembalian disetujui!')
        return redirect('admin_dashboard')
    return render(request, 'library/verify_return.html', {'borrowing': borrowing})
# views.py

def book_request(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            # Validasi manual berdasarkan request_type
            request_type = form.cleaned_data['request_type']
            if request_type == 'student':
                if not form.cleaned_data['student_name'] or not form.cleaned_data['class_name']:
                    messages.error(request, "Nama murid dan kelas wajib diisi untuk request murid.")
                    return render(request, 'library/book_request.html', {'form': form, 'all_requests': BookRequest.objects.all().order_by('-submitted_at')})
            elif request_type == 'parent':
                if not form.cleaned_data['parent_name'] or not form.cleaned_data['child_name'] or not form.cleaned_data['child_class']:
                    messages.error(request, "Nama orang tua, nama anak, dan kelas anak wajib diisi untuk request orang tua.")
                    return render(request, 'library/book_request.html', {'form': form, 'all_requests': BookRequest.objects.all().order_by('-submitted_at')})
            
            form.save()
            messages.success(request, "Request buku berhasil dikirim!")
            return redirect('book_request')  # Redirect ke halaman yang sama untuk refresh tabel
    else:
        form = BookRequestForm()
    
    # Kirim semua request untuk ditampilkan di tabel
    all_requests = BookRequest.objects.all().order_by('-submitted_at')  # Urutkan berdasarkan waktu terbaru
    return render(request, 'library/book_request.html', {'form': form, 'all_requests': all_requests})
