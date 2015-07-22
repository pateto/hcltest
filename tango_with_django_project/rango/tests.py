from django.test import TestCase
from rango.models import Category, Page
from django.core.urlresolvers import reverse
from rango.models import Category
from django.utils import timezone
import datetime

def add_cat(name, views, likes):
	c = Category.objects.get_or_create(name=name)[0]
	c.views = views
	c.likes = likes
	c.save()
	return c

class CategoryMethodTests(TestCase):

	# ensure_views_are_positive should results True for categories where views are zero or positive
	def test_ensure_views_are_positive(self):
		cat = Category(name='test', views=-1, likes=0)
		cat.save()
		self.assertEqual((cat.views >= 0), True)
	
	# slug_line_creation checks to make sure that when we add a category an appropriate slug line
	# i.e. "Random Category String" -> "random-category-string"
	def test_slug_line_creation(self):		
		cat = Category(name = 'Random Category String')
		cat.save()		
		self.assertEqual(cat.slug, 'random-category-string')
		
class IndexViewTests(TestCase):
	
	# If no questions exist, an appropriate message should be displayed
	def test_index_view_with_no_categories(self):
		response = self.client.get(reverse('rango:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no categories present.")
		self.assertQuerysetEqual(response.context['categories'], [])
	
	# If no questions exist, an appropriate message should be displayed
	def test_index_view_with_categories(self):
	
		add_cat('test', 1, 1)
		add_cat('temp', 1, 1)
		add_cat('tmp', 1, 1)
		add_cat('tmp test temp', 1, 1)
		
		response = self.client.get(reverse('rango:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "tmp test temp")
		
		num_cats = len(response.context['categories'])
		self.assertEqual(num_cats, 4)

class PageMethodTests(TestCase):

	# Test to ensure the last visit or first visit is not in the future
	def test_ensure_visits_not_in_future(self):
		cat = Category(name='test')
		cat.save()
		future_time = timezone.now() + datetime.timedelta(days=30)
		pag = Page(category=cat, first_visit=future_time, last_visit=future_time)
		self.assertEqual(pag.is_visit_in_future(), True)
		
	# Test to ensure that the last visit equal to or after the first visit
	def test_ensure_last_visit_equal_after_first_visit(self):
		cat = Category(name='test')
		cat.save()
		t1 = timezone.now()
		t2 = timezone.now() + datetime.timedelta(days=30)
		pag = Page(category=cat, first_visit=t1, last_visit=t2)
		self.assertEqual(pag.is_last_visit_equal_after_first_visit(), True)