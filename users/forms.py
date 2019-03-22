from django import forms
from .models import Document
from django.contrib.auth.models import User

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file', 'name')

class SearchForm(forms.ModelForm):
	name = forms.CharField(max_length=50)

	class Meta:
		model = User
		fields = ('name',)
