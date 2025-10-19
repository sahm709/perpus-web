from django.contrib import admin
from .models import Book, Student, Visit, Borrowing  

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_available', 'added_date']
    list_filter = ['is_available', 'added_date', 'is_recommended']
    search_fields = ['title', 'author']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'created_at']
    search_fields = ['name', 'grade']

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['student', 'book', 'book_read_manual', 'visit_date']  
    list_filter = ['visit_date']
    search_fields = ['student__name', 'book__title', 'book_read_manual'] 
    date_hierarchy = 'visit_date'

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ['student', 'book', 'book_manual', 'status', 'borrow_date']
    list_filter = ['status', 'borrow_date']
    search_fields = ['student__name', 'book__title', 'book_manual']
