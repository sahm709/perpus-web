from django.contrib import admin
from .models import Book, Student, Visit, Borrowing

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_available', 'added_date']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'created_at']

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['student', 'book_read', 'visit_date']

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ['student', 'book', 'book_manual', 'borrow_date', 'status']
    list_filter = ['status', 'borrow_date']