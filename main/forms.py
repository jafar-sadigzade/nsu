from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.flatpages.models import FlatPage

from .models import Comment, Contact


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class NewsSearchForm(forms.Form):
    query = forms.CharField(max_length=255, label='Search News', required=False)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'email', 'phone_number', 'subject', 'content']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Adınız'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Elektron poçt'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Əlaqə nömrəsi'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Mövzu'}),
            'content': forms.Textarea(attrs={'placeholder': 'Fikirlərinizi bizimlə bölüşün', 'rows': 10}),
        }


class FlatPageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'
