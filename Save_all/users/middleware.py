import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_user = request.user
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            cache.set(
                "seen_%s" % (current_user.username),
                now,
                settings.USER_LAST_SEEN_TIMEOUT,
            )
            current_user.profile.last_seen = now
            current_user.profile.save()
