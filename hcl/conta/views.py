from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from conta.models import NHva01
from .forms import NHva01Form
#import pdb
#pdb.set_trace()

def index(request):		
	response = render(request, 'conta/index.html', {})	
	return response

def hoja_de_vida(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NHva01Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NHva01Form()

    return render(request, 'conta/hoja_de_vida.html', {'form': form})

def hoja_de_vida_pag(request):	
	#nhva01_list = NHva01.objects.all()[:100]
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