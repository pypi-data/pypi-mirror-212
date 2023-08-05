from django.urls import path
from . import views
app_name = "app_test"


urlpatterns = []
urlpatterns.append(path('test', views.test))
