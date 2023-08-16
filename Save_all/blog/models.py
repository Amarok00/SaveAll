from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
# from django.utils.text import slugify
from pytils.translit import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Post(models.Model):
    class Meta:
        verbose_name = "Create post"
        verbose_name_plural = "Create posts"

    title = models.CharField(
        max_length=200,
        help_text="Maximum of 200 characters",
        db_index=True,
        verbose_name="Заголовок",
    )
    # content = models.TextField(max_length=5000, blank=True, null=True, help_text="Maximum of 5000 characters")
    content = RichTextField(
        max_length=5000, blank=True, null=True, help_text="Maximum of 5000 characters"
    )
    data_create = models.DateTimeField(default=timezone.now)
    data_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50)  # ,unique=True подумать
    likes_post = models.ManyToManyField(
        User, related_name="post_likes", blank=True, verbose_name="likes"
    )
    saves_posts = models.ManyToManyField(
        User,
        related_name="blog_posts_save",
        blank=True,
        verbose_name="Saved user posts",
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def total_likes_post(self):
        return self.likes_post.count()

    def total_saves_posts(self):
        return self.saves_posts.count()

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug, "pk": self.pk})

    def __str__(self):
        return self.title


# @receiver(pre_save, sender=Post)
# def prepopulated_slug(sender, instance, **kwargs):
#     instance.slug = slugify(instance.title)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments_blog', on_delete=models.CASCADE)
    name_author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=255)
    data_create = models.DateTimeField(auto_now_add=True)
    likes_comments = models.ManyToManyField(User,related_name="likes_blog_comment",blank = True)
    reply_comment = models.ForeignKey('self',null=True,related_name='replies_comment',on_delete=models.CASCADE)
    

    def total_likes_comment(self):
        return self.likes_comments.count()
    
    def __str__(self):
        return  "%s - %s - %s "(self.post.title, self.name_author , self.id)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug, "pk": self.pk})
    
