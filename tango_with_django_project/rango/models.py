from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(default='')
    
    def save(self, *args, **kwargs):
		if(self.views <= 0):
			self.views = 0
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
    
    def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	last_visit = models.DateTimeField(blank=True, null=True)
	first_visit = models.DateTimeField(blank=True, null=True)
	
	def is_visit_in_future(self):
		now = timezone.now()
		if (self.last_visit > now or self.first_visit > now):
			return True
		return False
	
	def is_last_visit_equal_after_first_visit(self):
		return (self.last_visit >= self.first_visit)
	
	def __unicode__(self):
		return self.title
		
class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)
	
	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	
	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username