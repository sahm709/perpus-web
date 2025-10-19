from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)  # True = Tersedia
    added_date = models.DateTimeField(auto_now_add=True)  # Untuk sort buku baru
    is_recommended = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title} oleh {self.author}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)  # Kelas, e.g., "X IPA 1"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Kelas {self.grade}"

class Visit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book_read = models.CharField(max_length=200, help_text="Judul buku yang dibaca (tuliskan manual jika belum di katalog)")
    visit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} membaca {self.book_read} pada {self.visit_date.date()}"

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