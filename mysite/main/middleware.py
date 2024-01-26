from django.shortcuts import redirect
from accounts.models import CustomUser

class UserLimitMiddleware:
    # A middle ware for preventing access to the signup page if the number of members exceeeds the limit set.
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_limit = CustomUser.objects.first().user_limit if CustomUser.objects.exists() else None

        current_user_count = CustomUser.objects.count()

        if user_limit is not None and current_user_count >= user_limit and request.path == '/accounts/signup/':
            return redirect('main:lesson_list')

        response = self.get_response(request)
        return response