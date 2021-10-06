from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import now
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import pre_save, post_save
from weThink.utils import unique_slug_generator

# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    desc = models.TextField(max_length=500, blank=True, null=True)
    content = RichTextUploadingField(config_name="default", blank=True, null=True)
    # content = models.TextField()
    postimage = models.ImageField(null=True, blank=True, upload_to='postImages')
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    views = models.IntegerField(default=0)
    slug = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return 'Post from '+ self.title+' by '+ str(self.author)

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)    


class BlogComment(models.Model):
    sno = models.AutoField(primary_key = True)
    comment = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)
    def __str__(self):
        return ' @ '+ self.user.username +' :- '+ self.comment[0:15]