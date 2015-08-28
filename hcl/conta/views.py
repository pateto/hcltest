from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from conta.models import NHva01
from .forms import NHva01Form
import pdb
#pdb.set_trace()

def index(request):		
	response = render(request, 'conta/index.html', {})	
	return response

def nhva01_detail(request, nhva01_id):
	
	#pdb.set_trace()
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NHva01Form(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			print 'is valid'
			
	# if a GET (or any other method) we'll create a blank form
	else:
		nhva01 = NHva01.objects.get(pk=nhva01_id)
		form = NHva01Form(instance=nhva01)
		
	return render(request, 'conta/nhva01.html', {'form': form})

def nhva01(request):	
	
	nhva01_list = NHva01.objects.all()
	paginator = Paginator(nhva01_list, 25)
	
	page = request.GET.get('p')
	try:
		nhva01 = paginator.page(page)
	except PageNotAnInteger:
		nhva01 = paginator.page(1)
	except EmptyPage:
		nhva01 = paginator.page(paginator.num_pages)
	
	return render_to_response('conta/list.html', {'nhva01': nhva01})