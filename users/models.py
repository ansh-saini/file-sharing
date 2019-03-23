from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	file = models.FileField(upload_to='files', blank=True)
	name = models.CharField(max_length=50, default='default')

	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	docs = models.ManyToManyField(Document, blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'

#Signals
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import os

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	if instance.file:
		if os.path.isfile(instance.file.path):
			os.remove(instance.file.path)
