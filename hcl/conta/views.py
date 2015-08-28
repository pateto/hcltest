from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from conta.models import NHva01
from .forms import NHva01Form
import pdb
#pdb.set_trace()

def index(request):		
	response = render(request, 'conta/index.html', {})	
	return response

def nhva01_detail(request, nhva01_id):
	
	nhva01 = get_object_or_404(NHva01, pk=nhva01_id)
	
	# Verificar si el proceso es POST
	if request.method == 'POST':
		# crear una instancia de tipo form
		form = NHva01Form(request.POST, instance = nhva01)
		# verificar su validez
		if form.is_valid():
			# Procesar los datos			
			form.save()
			
	# Si es un metodo 'GET' o algun otro, crear un formulario vacio
	else:
		form = NHva01Form(instance = nhva01)
		
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
	
	return render(request, 'conta/list.html', {'nhva01': nhva01})