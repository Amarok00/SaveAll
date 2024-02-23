from django.shortcuts import redirect


class AjaxMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.is_ajax = self.is_ajax(request)
        print(f"Request is AJAX: {request.is_ajax}")
        response = self.get_response(request)
        return response

    @staticmethod
    def is_ajax(request):
        return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
