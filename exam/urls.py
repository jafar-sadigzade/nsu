from django.urls import path
from exam import views

urlpatterns = [
    path("test", views.test, name="test"),
]
