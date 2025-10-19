import random  # Import untuk random selection
from django.core.management.base import BaseCommand
from library.models import Book
from django.utils import timezone

class Command(BaseCommand):
    help = 'Import initial books from the provided list randomly'

    def handle(self, *args, **options):
        all_books_data = [  # Daftar lengkap dari data Anda
            {'title': 'Aku Tahu Aku Bisa', 'author': ''},
            {'title': 'Aku Tahu Aku Bisa 10 Penemu Terbesar Dunia', 'author': ''},
            {'title': 'Aku Tahu Aku Bisa Alat dan Mesin Bawah Laut', 'author': ''},
            {'title': 'Aku Tahu Aku Bisa Era Penemuan Baru', 'author': ''},
            {'title': 'Aku Tahu Aku Bisa Obat dan Kedokteran', 'author': ''},
            {'title': 'Aku Tahu Aku Bisa Penemuan Abad Industri', 'author': ''},
            {'title': 'Aku Tahu Aku Bisa Penemuan Milenium Pertama', 'author': ''},
            {'title': 'Aku Tahu Aku Bisa Penemuan Modern', 'author': ''},
            {'title': 'Aku Tahu Aku Bisa Penjelajahan Antartika', 'author': ''},
            {'title': 'Aku Tahu Aku Bisa Peradaban Awal', 'author': ''},
            # Tambahkan sisanya jika diperlukan, tapi kita pilih random dari ini
            {'title': 'Al Quran dan Tafsirnya Jilid III Juz 7-8-9', 'author': 'Departemen Agama RI'},
            # ... (lanjutkan dengan daftar lengkap Anda)
            # Untuk kesederhanaan, saya gunakan daftar pendek di sini
        ]
        
        if len(all_books_data) > 10:
            selected_books = random.sample(all_books_data, 10)  # Pilih 10 buku acak
        else:
            selected_books = all_books_data  # Jika kurang, ambil semuanya
        
        for book_data in selected_books:
            is_recommended = random.choice([True, False])  # Setel acak True atau False
            Book.objects.create(
                title=book_data['title'],
                author=book_data['author'],
                is_available=True,  # Setel default True
                added_date=timezone.now(),
                is_recommended=is_recommended  # Setel field baru
            )
            self.stdout.write(self.style.SUCCESS(f'Buku "{book_data["title"]}" ditambahkan dengan is_recommended={is_recommended}.'))

        self.stdout.write(self.style.SUCCESS('10 buku acak berhasil diimpor!'))