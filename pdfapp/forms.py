<<<<<<< HEAD
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
=======
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
>>>>>>> origin/main
        fields = ['title', 'author', 'publication_year']