from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.views.generic import CreateView
from .models import Document, Profile
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm, SearchForm, LinkForm, DeleteForm
from django.contrib.auth.models import User

@login_required
def home(request):
	form = SearchForm()
	return render(request, 'users/home.html', {'form': form})


def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account for {username} has been successfully created!')
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
	profile = Profile.objects.get(user=request.user)
	docs = Document.objects.filter(user=request.user)
	return render(request, 'users/profile.html', {'profile': profile, 'media': settings.MEDIA_URL})


@login_required
def user_profile(request, username):
	user = User.objects.get(username=username)
	profile = Profile.objects.get(user=user)
	if user == request.user:
		return render(request, 'users/profile.html', {'profile': profile, 'media': settings.MEDIA_URL})
	else:
		return render(request, 'users/user_profile.html', {'profile': profile})


@login_required
def file_upload(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			object = form.save()
			profile = Profile.objects.get(user=request.user)
			file = Document.objects.get(id=object.id)
			profile.docs.add(file)
			return redirect('profile')
	else:
		form = DocumentForm()
	return render(request, 'users/upload.html', {'form': form})


@login_required
def file_delete(request):
	if request.method == 'POST':
		form = DeleteForm(request, request.POST)
		delete_list = form['checklist'].value()
		for file_id in delete_list:
			file = Document.objects.get(id=file_id)
			file.delete()
	else:
		form = DeleteForm(request)
	return render(request, 'users/delete.html', {'form': form})


@login_required
def search_user(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		query = form.data['name']
		try:
			user = User.objects.get(username=query)
		except Exception as e:
			user = None
			messages.error(request, f' {query} Not Found!')
		if user:
			return redirect('user-profile', username=user)
		return redirect('home')
	else:
		form = SearchForm()
	return redirect('home')


@login_required
def share_link(request):
	if request.method == 'POST':
		form = LinkForm(request, request.POST)
		username = form.data['name']
		user = User.objects.get(username=username)
		profile = Profile.objects.get(user=user)
		checklist = form['checklist'].value()
		for file_id in checklist:
			file = Document.objects.get(id=file_id)
			profile.docs.add(file)
	else:
		form = LinkForm(request)
	return render(request, 'users/share.html', {'form': form})


@login_required
def share_unlink(request):
	if request.method == 'POST':
		form = LinkForm(request, request.POST)
		username = form.data['name']
		user = User.objects.get(username=username)
		profile = Profile.objects.get(user=user)
		checklist = form['checklist'].value()
		for file_id in checklist:
			file = Document.objects.get(id=file_id)
			profile.docs.remove(file)
	else:
		form = LinkForm(request)
	return render(request, 'users/share.html', {'form': form})
