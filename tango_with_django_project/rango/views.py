from django.shortcuts import render, render_to_response
from rango.models import Category, Page, UserProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query
from django.template.context import RequestContext
from django.utils import timezone

import pdb
#pdb.set_trace()

def get_category_list(max_results=0, starts_with=''):

	cat_list = []
	
	if starts_with:
		cat_list = Category.objects.filter(name__istartswith = starts_with)	
	
	if max_results > 0:
		if (len(cat_list) > max_results):
			cat_list = cat_list[:max_results]
	
	return cat_list

def index(request):
	
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	
	context_dict = {'categories': category_list, 'pages': page_list}
	
	visits = request.session.get('visits')
	if not visits:
		visits = 1
	reset_last_visit_time = False
	
	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		
		if (datetime.now() - last_visit_time).seconds > 0:
			# ...reassign the value of the cookie to +1 of what it was before...
			visits = visits + 1
			# ...and update the last visit cookie, too.
			reset_last_visit_time = True
	else:
		# Cookie last_visit doesn't exist, so create it to the current date/time.
		reset_last_visit_time = True
	
	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits
		
	context_dict['visits'] = visits
	
	response = render(request, 'rango/index.html', context_dict)
	
	return response
	
def about(request):
	
	if request.session.get('visits'):
		count = request.session.get('visits')
	else:
		count = 0
	
	return render(request, 'rango/about.html', {'visits': count})

def category(request, category_name_slug):
	
	#Create a context dictionary which we can pass to the template rendering engine.
	context_dict = {}
	
	try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		context_dict['category_name_slug'] = category.slug
		
		# Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
		pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
		context_dict['pages'] = pages
		
		# We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.		
		context_dict['category'] = category
		
	except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
		pass
		
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			# Run our Bing function to get the results list!
			result_list = run_query(query)
			context_dict['result_list'] = result_list
				
	# Go render the response and return it to the client.
	return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
	
		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			form.save(commit=True)
		
		# Now call the index() viewed.
		# The user will be shown the homepage
		return index(request)
	else:
		# If the request was not a POST, display the form to enter details.
		form = CategoryForm()
		
	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'rango/add_category.html',{'form':form})
	
def add_page(request, category_name_slug):

	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None
	
	if request.method == 'POST':		
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:				
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.first_visit = timezone.now()
				page.last_visit = timezone.now()
				page.save()
				# probably better to use a redirect here.
				return HttpResponseRedirect(reverse('rango:category', kwargs={'category_name_slug': category_name_slug}))
				
		else:
			print form.errors
	else:
		form = PageForm()
		
		context_dict = {'form':form, 'category':cat, 'category_name_slug':category_name_slug}
	
		return render(request, 'rango/add_page.html', context_dict)

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html', {})

def track_url(request):	
	if request.method == 'GET':		
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			page = Page.objects.get(id=page_id)			
			page.views += 1			
			page.last_visit = timezone.now()
			page.save()
			return HttpResponseRedirect(page.url)
	else:
		return render(request, 'rango/index.html', {})
		
@login_required
def add_profile(request):
	# A HTTP POST?
	if request.method == 'POST':
		form = UserProfileForm(request.POST)
	
		# Have we been provided with a valid form?
		if form.is_valid():
			userProfile = form.save(commit=False)
			userProfile.user_id = request.user.id
			
			if 'picture' in request.FILES:
				userProfile.picture = request.FILES['picture']
				
			# Save the new category to the database.
			form.save(commit=True)
		
		# Now call the index() viewed.
		# The user will be shown the homepage
		return index(request)
	else:
		# If the request was not a POST, display the form to enter details.
		form = UserProfileForm()
		
	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'rango/profile_registration.html',{'form':form})

@login_required
def profile(request):
	context_dict = {}
	try:
		userProfile = UserProfile.objects.get(user = request.user)
		context_dict['userProfile'] = userProfile		
	except Exception:
		pass
		
	return render_to_response('rango/profile.html', context_instance = RequestContext(request, context_dict))

@login_required
def like_category(request):

	cat_id = None
	if request.method == 'GET':		
		cat_id = request.GET['category_id']
		
	likes = 0
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1
			cat.likes = likes
			cat.save()
			
	return HttpResponse(likes)

def suggest_category(request):	
	cat_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']
		cat_list = get_category_list(8, starts_with)
	return render(request, 'rango/category_list.html', {'cat_list': cat_list})
	
@login_required
def auto_add_page(request):
	
	cat_id = None
	url = None
	title = None
	context_dict = {}
	if request.method == 'GET':		
		cat_id = request.GET['category_id']
		title = request.GET['title']
		url = request.GET['url']
		if cat_id:
			category = Category.objects.get(id=int(cat_id))
			p = Page.objects.get_or_create(category=category, title=title, url=url)[0]
			p.first_visit = timezone.now()
			p.last_visit = timezone.now()
			p.save()
			pages = Page.objects.filter(category=category).order_by('-views')
			# Add our results to the template context under name pages.
			context_dict['pages'] = pages
	return render(request, 'rango/page_list.html', context_dict)
		