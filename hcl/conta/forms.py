from django import forms
from conta.models import NHva01

class NHva01Form(forms.ModelForm):	
	class Meta:		
		model = NHva01
		exclude = ('id',)