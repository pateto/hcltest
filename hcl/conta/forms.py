from django import forms
from conta.models import NHva01

class NHva01Form(forms.ModelForm):
	id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
	class Meta:		
		model = NHva01		
		exclude = ('',)