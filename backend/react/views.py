from django.shortcuts import render, redirect
from django.http import HttpRequest

from identity.models import Author

# Route prefixes that require authorization
_PROTECTED_ROUTE_PREFIXES = [
    "/profile",
    "/home"
]

# Route to redirect to if unauthorized
_UNAUTHORIZED_REDIRECT_PATH = "/"

def index(request: HttpRequest):
    for route_prefix in _PROTECTED_ROUTE_PREFIXES:
        if request.get_full_path().startswith(route_prefix):
            # User has not logged in
            if not "id" in request.session:
                return redirect(_UNAUTHORIZED_REDIRECT_PATH)
            
            # User no longer has account/invalid session
            try:
                Author.objects.get(id=request.session["id"])
            except Author.DoesNotExist:
                request.session.clear()
                return redirect(_UNAUTHORIZED_REDIRECT_PATH)
            break

    return render(request, "index.html")