from django.db import models
from django.contrib.auth.models import User
from datetime import date,datetime

from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    friends = models.ManyToManyField(User, related_name="my_friends", blank=True)
    bio = models.CharField(max_length=150, blank=True)
    date_of_birth = models.CharField(max_length=10, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        default="default_profile.jpg", upload_to="profiles_img", blank=True, null=True
    )
    first_name = models.CharField(max_length=25, blank=True, null=True)

    last_name = models.CharField(max_length=25, blank=True, null=True)

    def age(self):
        if self.date_of_birth:
            date_of_birth = datetime.strptime(self.date_of_birth, '%d.%m.%Y').date()
            today = date.today()
            return (
                today.year
                - date_of_birth.year
                - (
                    (today.month, today.day)
                    < (date_of_birth.month, date_of_birth.day)
                )
            )
        return None

    def profile_post(self):
        return self.user.post_set.all()

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()
    
    def __str__(self) -> str:
        return f"{self.user.username} Profile"


STATUS_CHOICES = (("send", "send"), ("accepted", "accepted"))


class Relationship(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="friends_sender"
    )
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="friends_receiver"
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} - {self.receiver} - {self.status}"
