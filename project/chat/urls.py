from django.urls import path

from chat import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('inbox/<int:chat_id>/', views.InboxView.as_view(), name='chat'),
    path('inbox/', views.ChatListView.as_view(), name='inbox'),


]
