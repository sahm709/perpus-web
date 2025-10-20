from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)  # True = Tersedia
    added_date = models.DateTimeField(auto_now_add=True)  # Untuk sort buku baru
    is_recommended = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)  # Kelas, e.g., "X IPA 1"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Kelas {self.grade}"

class Visit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)  # Pilih dari DB
    book_read_manual = models.CharField(max_length=200, blank=True, help_text="Tulis judul buku manual jika tidak ada di katalog")
    visit_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.book:
            return f"{self.student} membaca {self.book} pada {self.visit_date.date()}"
        else:
            return f"{self.student} membaca {self.book_read_manual} pada {self.visit_date.date()}"


class Borrowing(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)  # Bisa null jika manual
    book_manual = models.CharField(max_length=200, blank=True, help_text="Tulis judul buku manual jika tidak ada di katalog")
    borrow_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('pending_return', 'Pending Return'),
        ('returned', 'Returned'),
    ])
    return_date = models.DateTimeField(null=True, blank=True)  # Untuk catat tanggal pengembalian

    def __str__(self):
        if self.book:
            return f"{self.student} meminjam {self.book} - {self.status}"
        else:
            return f"{self.student} meminjam {self.book_manual} - {self.status}"

class BookRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('student', 'Murid'),
        ('parent', 'Orang Tua'),
    ]
    
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES, verbose_name="Tipe Request")
    # Field untuk murid
    student_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nama Murid")
    class_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kelas")
    
    # Field untuk orang tua
    parent_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nama Orang Tua")
    child_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nama Anak")
    child_class = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kelas Anak")
    
    # Field umum
    book_title_or_type = models.CharField(max_length=200, verbose_name="Judul Buku atau Jenis Buku yang Direquest")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Submit")
    
    def __str__(self):
        if self.request_type == 'student':
            return f"Request dari {self.student_name} (Murid, Kelas {self.class_name}): {self.book_title_or_type}"
        elif self.request_type == 'parent':
            return f"Request dari {self.parent_name} (Orang Tua, Anak: {self.child_name}, Kelas {self.child_class}): {self.book_title_or_type}"
        return f"Request: {self.book_title_or_type}"