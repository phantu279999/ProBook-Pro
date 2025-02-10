from django.db import models
from ckeditor.fields import RichTextField

from src.common.common import build_url_news
from src.process_data.base_action import BaseAction

# When model is updated, there will be an action to save it to the Redis queue and
# there will be another thread running to automatically update the data on Redis.


class News(models.Model):
	title = models.CharField(max_length=255, db_index=True)
	sapo = models.CharField(max_length=255)
	url = models.CharField(max_length=255, blank=True)
	avatar = models.ImageField(upload_to='avatar_news')
	date_create = models.DateTimeField(auto_now_add=True)
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
		# Auto update data Redis
		BaseAction().push_action_to_queue({
			"action": "update_news",
			"data": {
				"pk": self.pk,
				"title": self.title
			}
		})


class NewsContent(models.Model):
	newsid = models.ForeignKey(News, on_delete=models.CASCADE)
	body = RichTextField(blank=True, null=True)

	def __str__(self):
		return self.newsid.title

	def save(self, *args, **kwargs):
		super(NewsContent, self).save(*args, **kwargs)
		# Auto update data Redis
		BaseAction().push_action_to_queue({
			"action": "update_newscontent",
			"data": {
				"pk": self.pk,
				"newsid": self.newsid.pk
			}
		})


class Category(models.Model):
	name = models.CharField(max_length=255)
	url = models.SlugField(blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		super(Category, self).save(*args, **kwargs)
		# Auto update data Redis
		BaseAction().push_action_to_queue({
			"action": "update_category",
			"data": {
				"pk": self.pk,
				"name": self.name
			}
		})


class CategoryNews(models.Model):
	newsid = models.ForeignKey(News, on_delete=models.CASCADE)
	categoryid = models.ForeignKey(Category, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		super(CategoryNews, self).save(*args, **kwargs)
		# Auto update data Redis
		BaseAction().push_action_to_queue({
			"action": "update_categorynews",
			"data": {
				"pk": self.pk,
				"cate_id": self.categoryid.pk
			}
		})


class Tag(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255, blank=True)

	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.url = build_url_news(self.name)
		super(Tag, self).save(*args, **kwargs)
		# Auto update data Redis
		BaseAction().push_action_to_queue({
			"action": "update_tag",
			"data": {
				"pk": self.pk,
				"name": self.name
			}
		})


class TagNews(models.Model):
	newsid = models.ForeignKey(News, on_delete=models.CASCADE)
	tagid = models.ForeignKey(Tag, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('newsid', 'tagid')

	def save(self, *args, **kwargs):
		super(TagNews, self).save(*args, **kwargs)
		# Auto update data Redis
		BaseAction().push_action_to_queue({
			"action": "update_tagnews",
			"data": {
				"pk": self.pk,
				"tag_id": self.tagid_id
			}
		})


class Topic(models.Model):
	name = models.CharField(max_length=255)
	url = models.URLField(blank=True)

	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.url = build_url_news(self.name)
		super(Topic, self).save(*args, **kwargs)
		# Auto update data Redis
		BaseAction().push_action_to_queue({
			"action": "update_topic",
			"data": {
				"pk": self.pk,
				"name": self.name
			}
		})


class TopicNews(models.Model):
	newsid = models.ForeignKey(News, on_delete=models.CASCADE)
	topicid = models.ForeignKey(Topic, on_delete=models.CASCADE)

	def __str__(self):
		return "{} -> {}".format(self.topicid.name, self.newsid.title)

	class Meta:
		unique_together = ('newsid', 'topicid')

	def save(self, *args, **kwargs):
		super(TopicNews, self).save(*args, **kwargs)
		# Auto update data Redis
		BaseAction().push_action_to_queue({
			"action": "update_topicnews",
			"data": {
				"pk": self.pk,
				"topic_id": self.topicid_id
			}
		})
