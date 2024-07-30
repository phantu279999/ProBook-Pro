from django.db import models
from ckeditor.fields import RichTextField

from src.common.common import build_url_news


class News(models.Model):
	title = models.CharField(max_length=255, db_index=True)
	sapo = models.CharField(max_length=255)
	url = models.CharField(max_length=255, blank=True)
	avatar = models.ImageField(upload_to='avatar_news')
	date_create = models.DateTimeField(blank=True)
	lastmodifield_date = models.DateTimeField(auto_now=True)
	status = models.BooleanField()

	is_home = models.BooleanField()
	is_focus = models.BooleanField()

	created_by = models.CharField(max_length=255)
	edited_by = models.CharField(max_length=255)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.url:
			self.url = "{}-{}".format(build_url_news(self.title), self.pk)
		super(News, self).save(*args, **kwargs)


class NewsContent(models.Model):
	newsid = models.ForeignKey(News, on_delete=models.CASCADE)
	body = RichTextField(blank=True, null=True)


class Category(models.Model):
	name = models.CharField(max_length=255)
	url = models.URLField(blank=True)
	
	def __str__(self):
		return self.name


class CategoryNews(models.Model):
	newsid = models.ForeignKey(News, on_delete=models.CASCADE)
	categoryid = models.ForeignKey(Category, on_delete=models.CASCADE)


class Tag(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255, blank=True)

	created_date = models.DateTimeField()
	modified_date = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.url = build_url_news(self.name)
		super(Tag, self).save(*args, **kwargs)


class TagNews(models.Model):
	newsid = models.ForeignKey(News, on_delete=models.CASCADE)
	tagid = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Topic(models.Model):
	name = models.CharField(max_length=255)
	url = models.URLField(blank=True)

	created_date = models.DateTimeField()
	modified_date = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.url = build_url_news(self.name)
		super(Topic, self).save(*args, **kwargs)


class TopicNews(models.Model):
	newsid = models.ForeignKey(News, on_delete=models.CASCADE)
	topicid = models.ForeignKey(Topic, on_delete=models.CASCADE)

