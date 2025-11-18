from django.urls import path
from api.views import public_view, secure_view

urlpatterns = [
    path("", public_view),
    path("secure/", secure_view),
]
