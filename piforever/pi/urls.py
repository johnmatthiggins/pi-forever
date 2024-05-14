from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('digits/<start_range>', views.digits, name="Digits"),
]
