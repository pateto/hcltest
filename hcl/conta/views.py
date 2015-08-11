from django.shortcuts import render

def index(request):	
	
	response = render(request, 'conta/index.html', {})
	
	return response
