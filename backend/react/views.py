from django.shortcuts import render, redirect
from django.http import HttpRequest

from identity.models import Author

_PROTECTED_ROUTE_PREFIXES = [
    "/profile",
    "/home"
]

_UNAUTHORIZED_REDIRECT_PATH = "/"

def index(request: HttpRequest):
    for route_prefix in _PROTECTED_ROUTE_PREFIXES:
        if request.get_full_path().startswith(route_prefix):
            if not "id" in request.session:
                return redirect(_UNAUTHORIZED_REDIRECT_PATH)
            
            try:
                Author.objects.get(id=request.session["id"])
            except Author.DoesNotExist:
                # User no longer has account/invalid session
                request.session.clear()
                return redirect(_UNAUTHORIZED_REDIRECT_PATH)
            break

    return render(request, "index.html")