from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import FriendRequest
from users.models import Profile
from chats.models import Chat
from feed.models import (
    FriendEvent,
    FriendRequestEvent,
    RemoveFriendEvent,
    FriendRequestDeclinedEvent,
)


class SendFriendRequest(View):
    """Class based view for the sending a friend request"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for the sending a friend request"""
        if request.is_ajax:
            print('start send ajax')
            from_profile = request.user.profile
            profile_id = request.POST.get("profile_id")
            to_profile = get_object_or_404(Profile, id=profile_id)
            # need to check if the request is already sent
            if FriendRequest.objects.filter(
                from_profile=from_profile, to_profile=to_profile
            ).exists():
                return JsonResponse({"status": "error"})
            friend_request = FriendRequest(
                from_profile=from_profile, to_profile=to_profile
            )
            friend_request.save()
            friend_request_event = FriendRequestEvent.objects.create(
                initiator=from_profile.user,
                target=to_profile.user,
            )
            friend_request_event.save()
            return JsonResponse({"status": "ok"})
        return JsonResponse({"status": "error"})


class AcceptFriendRequest(View):
    """Class based view for accepting a friend request"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for accepting a friend request"""
        if request.is_ajax:
            accepting_user = request.user
            profile_id = request.POST.get("profile_id")
            accepted_profile = get_object_or_404(Profile, id=profile_id)
            friend_request = get_object_or_404(
                FriendRequest,
                from_profile=accepted_profile,
                to_profile=accepting_user.profile,
            )
            if friend_request:
                friend_request.accepted = True
                friend_request.declined = False
                accepting_user.profile.friends.add(accepted_profile.user)
                accepted_profile.friends.add(accepting_user.profile.user)
                friend_request.delete()
                accepting_user.profile.save()
                accepted_profile.save()
                friend_event = FriendEvent.objects.create(
                    initiator=accepting_user,
                    target=accepted_profile.user,
                )
                friend_event.save()
                return JsonResponse({"status": "ok"})
            # if the request is not found return error
            return JsonResponse({"status": "error"})
        return JsonResponse({"status": "error"})


class DeclineFriendRequest(View):
    """Class based view for the declining a friend request"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for the declining a friend request"""
        if request.is_ajax:
            declining_profile = request.user.profile
            profile_id = request.POST.get("profile_id")
            declined_profile = get_object_or_404(Profile, id=profile_id)
            friend_request = get_object_or_404(
                FriendRequest,
                from_profile=declined_profile,
                to_profile=declining_profile,
            )
            if friend_request:
                friend_request.accepted = False
                friend_request.declined = True
                friend_request.delete()
                request_declined = FriendRequestDeclinedEvent.objects.create(
                    initiator=declining_profile.user,
                    target=declined_profile.user,
                )
                request_declined.save()
                return JsonResponse({"status": "ok"})
            # if the request is not found return error
            return JsonResponse({"status": "error"})
        return JsonResponse({"status": "error"})


class RemoveFriend(View):
    """Class-based view for removing a friend"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for removing a friend"""
        if request.is_ajax:
            print("start ajax")
            remover = request.user.profile
            friend_id = request.POST.get("profile_id")
            friend = get_object_or_404(Profile, id=friend_id)

            # Use user attribute instead of Profile instance
            remover.friends.remove(friend.user)
            friend.friends.remove(remover.user)

            remover.save()
            friend.save()

            # Create an event for the friend removed
            remove_friend_event = RemoveFriendEvent.objects.create(
                initiator=remover.user,
                target=friend.user,
            )
            remove_friend_event.save()

            # Find and delete a chat between the two users
            chat = Chat.objects.filter(
                members=remover.user,
            ).filter(
                members=friend.user,
            )
            print("is ajax")
        else:
            print("no ajax")
            if chat:
                chat.delete()

            return JsonResponse({"status": "ok"})


class CancelFriendRequest(View):
    """Class based view for the canceling a friend request"""

    def post(self, request, *args, **kwargs):
        """POST ajax handler for the canceling a friend request"""
        if request.is_ajax:
            print("start cancle ajax")
            profile1 = request.user.profile
            profile2 = get_object_or_404(Profile, id=request.POST.get("profile_id"))
            friend_request = get_object_or_404(
                FriendRequest, from_profile=profile1, to_profile=profile2
            )
            friend_request_event = FriendRequestEvent.objects.filter(
                initiator=profile1.user,
                target=profile2.user,
            )
            friend_request.delete()
            friend_request_event.delete()
            return JsonResponse({"status": "ok"})
        else:
            print("no ajax")
        return JsonResponse({"status": "error"})


class MyFriendsView(View):
    """Class based view for the my friends page"""

    def get(self, request, *args, **kwargs):
        """GET method for the my friends page"""
        friends = request.user.profile.friends.all()
        pending_requests = FriendRequest.get_pending_requests().filter(
            to_profile=request.user.profile
        )
        return render(
            request,
            "friends/my_friends.html",
            {"friends": friends, "pending_requests": pending_requests},
        )
