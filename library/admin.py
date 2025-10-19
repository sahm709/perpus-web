from django.contrib import admin
from .models import Book, Student, Visit, Borrowing, BookRequest

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_available', 'is_recommended', 'added_date'] 
    list_filter = ['is_available', 'is_recommended']  
    ordering = ['-is_recommended', 'title']   

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

@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ['request_type', 'student_name', 'class_name', 'parent_name', 'child_name', 'child_class', 'book_title_or_type', 'submitted_at']
    list_filter = ['request_type', 'submitted_at']
    search_fields = ['student_name', 'parent_name', 'child_name', 'book_title_or_type']