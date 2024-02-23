from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone
from django.urls import reverse

from chats.models import Message
from Save_all import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    last_seen = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)
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
            date_of_birth = datetime.strptime(self.date_of_birth, "%d.%m.%Y").date()
            today = date.today()
            return (
                today.year
                - date_of_birth.year
                - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            )
        return None

    @property
    def pending_friends_in(self):
        """Returns the list of pending incoming friend requests"""
        profiles_list = []
        for friend_request in self.friend_request_to_profile.all():
            if not friend_request.accepted and not friend_request.declined:
                profiles_list.append(friend_request.from_profile)
        return profiles_list

    @property
    def pending_requests_count(self):
        """Returns the number of pending friend requests"""
        return len(self.pending_friends_in)

    @property
    def pending_friends_out(self):
        """Returns the list of pending outgoing friend requests"""
        profiles_list = []
        for friend_request in self.friend_request_from_profile.all():
            if not friend_request.accepted and not friend_request.declined:
                profiles_list.append(friend_request.to_profile)
        return profiles_list

    @property
    def unread_messages_count(self):
        """Returns the number of unread messages for the user"""
        messages = (
            Message.objects.filter(chat__members=self.user, is_read=False)
            .exclude(author=self.user)
            .count()
        )
        return messages

    def profile_post(self):
        return self.user.post_set.all()

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    @property
    def online(self):
        """Returns True if the user was seen in the last 5 minutes"""
        if self.last_seen:
            now = timezone.now()
            last_seen = self.last_seen.astimezone(timezone.get_current_timezone())

            if now > last_seen + timezone.timedelta(
                seconds=settings.USER_ONLINE_TIMEOUT
            ):
                return False
            else:
                return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self.user.username} Profile"
    
    def __eq__(self, other):
        if isinstance(other, Profile):
            return self.user == other.user
        return False


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
