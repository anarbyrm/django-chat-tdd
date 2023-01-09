from django.urls import path

from chat import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

]
