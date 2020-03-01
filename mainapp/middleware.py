from django.shortcuts import redirect

class MyAppMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.user.is_authenticated or request.get_full_path().endswith('login/') or request.get_full_path().endswith('signup/') or request.get_full_path().endswith('admin/'):
            response = self.get_response(request)
            return response

        return redirect('login')

class MySessionExpiryMiddleWare:

    def __init__(self, get_response):

        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.user.is_authenticated and not request.user.is_superuser:
            request.session.set_expiry(300)

        response = self.get_response(request)

        return response