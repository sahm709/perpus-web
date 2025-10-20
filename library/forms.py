from django import forms
from .models import Student, Book, BookRequest

class VisitRecordForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nama Siswa', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.CharField(max_length=20, label='Kelas', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book = forms.ModelChoiceField(queryset=Book.objects.all(), required=False, label='Pilih Buku dari Katalog', empty_label='-- Pilih Buku --', widget=forms.Select(attrs={'class': 'form-select'}))
    book_read_manual = forms.CharField(max_length=200, label='Atau Tulis Buku Manual', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        book_read_manual = cleaned_data.get('book_read_manual')
        if not book and not book_read_manual:
            raise forms.ValidationError('Pilih buku dari katalog atau tulis judul manual.')
        return cleaned_data

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

class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ['request_type', 'student_name', 'class_name', 'parent_name', 'child_name', 'child_class', 'book_title_or_type']
        widgets = {
            'request_type': forms.Select(attrs={'id': 'request_type'}),
            'student_name': forms.TextInput(attrs={'id': 'student_name'}),
            'class_name': forms.TextInput(attrs={'id': 'class_name'}),
            'parent_name': forms.TextInput(attrs={'id': 'parent_name'}),
            'child_name': forms.TextInput(attrs={'id': 'child_name'}),
            'child_class': forms.TextInput(attrs={'id': 'child_class'}),
            'book_title_or_type': forms.TextInput(attrs={'placeholder': 'Contoh: "Harry Potter" atau "Buku Matematika"'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set field sebagai required berdasarkan request_type (akan ditangani di JavaScript/template)
        self.fields['student_name'].required = False
        self.fields['class_name'].required = False
        self.fields['parent_name'].required = False
        self.fields['child_name'].required = False
        self.fields['child_class'].required = False
