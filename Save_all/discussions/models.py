from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

class Discussions(models.Model):
    class Meta:
        verbose_name = "Discussion"
        verbose_name_plural = "Discussions"
    title = models.CharField(max_length=200, help_text='Max  of 200 characters', db_index=True)
    content = RichTextField(
        max_length=5000, blank=True, null=True, help_text="Maximum of 5000 characters"
    )
    data_create = models.DateTimeField(default=timezone.now)
    data_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50)  # ,unique=True подумать
    likes_discussions = models.ManyToManyField(
        User, related_name="discussions_likes", blank=True, verbose_name="likes"
    )
    saves_discussions = models.ManyToManyField(
        User,
        related_name="blog_discussions_save",
        blank=True,
        verbose_name="Saved user discussions",
    )
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Discussions, self).save(*args, **kwargs)
        
    def total_likes_discussions(self):
        return self.likes_discussions.count()

    def total_saves_discussions(self):
        return self.saves_discussions.count()

    def get_absolute_url(self):
        return reverse("discussions-detail", kwargs={"slug": self.slug,"pk": self.pk})

    def __str__(self):
        return self.title

