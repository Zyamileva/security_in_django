import logging

from django.utils.timezone import now
from django.shortcuts import render, redirect

logger = logging.getLogger(__name__)


class ProtectedPageAccessLoggerMiddleware:
    """Logs unauthorized access attempts to protected pages.

    Redirects unauthenticated users attempting to access pages under '/home/' to the login page and logs the attempt.
    """
    def __init__(self, get_response):
        """Initializes the middleware.

        Args:
            get_response: The next middleware in the chain.
        """
        self.get_response = get_response

    def __call__(self, request):
        """Processes the request.

        Logs unauthorized access attempts to protected pages and redirects to the login page if necessary.

        Args:
            request: The incoming request.

        Returns:
            The response from the next middleware or a redirect response.
        """
        if not request.user.is_authenticated and request.path.startswith("/home/"):
            logger.warning(
                f"[{now()}] Несанкціонований доступ: {request.META.get('REMOTE_ADDR')} -> {request.path}"
            )
            return redirect("login")

        return self.get_response(request)


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        """Initializes the middleware.

        Args:
            get_response: The next middleware in the chain.
        """
        self.get_response = get_response

    def __call__(self, request):
        """Processes the request.

        Handles exceptions and renders custom error pages if necessary.

        Args:
            request: The incoming request.

        Returns:
            The response from the next middleware or a custom error response.
        """
        try:
            response = self.get_response(request)
            if response.status_code == 404:
                return render(request, 'main/404.html', status=404)
            return response
        except Exception as e:
            logging.error(f'Error: {e}')
            return render(request, 'main/500.html', status=500)


