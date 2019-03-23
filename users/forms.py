from django import forms
from .models import Document
from django.contrib.auth.models import User

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ['file', 'name']

class SearchForm(forms.ModelForm):
	name = forms.CharField(max_length=50)

	class Meta:
		model = User
		fields = ['name']


class LinkForm(forms.Form):
	name = forms.CharField(max_length=50)
	
	class Meta:
		fields = ['name', 'checklist']

	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		docs = Document.objects.filter(user=request.user)
		self.fields['checklist'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=docs)


class DeleteForm(forms.Form):
	
	class Meta:
		fields = ['checklist']

	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		docs = Document.objects.filter(user=request.user)
		self.fields['checklist'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=docs)
