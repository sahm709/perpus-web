from django import forms
from .models import Student, Book

class VisitRecordForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nama Siswa', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.CharField(max_length=20, label='Kelas', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_read = forms.CharField(max_length=200, label='Buku yang Dibaca', required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

class HistoryCheckForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nama Siswa', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.CharField(max_length=20, label='Kelas', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        grade = cleaned_data.get('grade')
        if name and grade:
            try:
                Student.objects.get(name=name, grade=grade)
            except Student.DoesNotExist:
                raise forms.ValidationError('Siswa tidak ditemukan.')

class BorrowRequestForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nama Siswa', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.CharField(max_length=20, label='Kelas', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book = forms.ModelChoiceField(queryset=Book.objects.all(), required=False, label='Pilih Buku', empty_label='-- Pilih Buku --', widget=forms.Select(attrs={'class': 'form-select'}))
    book_manual = forms.CharField(max_length=200, label='Atau Tulis Buku Manual', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        book_manual = cleaned_data.get('book_manual')
        if not book and not book_manual:
            raise forms.ValidationError('Pilih buku atau tulis manual.')

class ReturnRequestForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nama Siswa', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.CharField(max_length=20, label='Kelas', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    borrowing_id = forms.IntegerField(label='ID Peminjaman', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    book_manual = forms.CharField(max_length=200, label='Atau Tulis Buku Manual', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))