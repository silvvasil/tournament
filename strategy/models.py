from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'strategies/{0}_main.cpp'.format(instance.user, filename)

class Strategy(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	main = models.FileField(null=True, blank=True, upload_to=user_directory_path)

	def __str__(self):
		return str(self.user) + "_strategy"