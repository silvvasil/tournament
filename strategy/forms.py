from django import forms
from .models import Strategy
from django.contrib.auth.models import User

class UploadForm(forms.ModelForm):
	class Meta:
		model = Strategy
		fields = ('main', )

