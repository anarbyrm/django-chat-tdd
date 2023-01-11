from django.urls import path

from chat_users import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('<int:user_id>/send-request/', views.send_friend_request, name='send-request'),
    path('requests/', views.RequestsListView.as_view(), name='requests'),
    path('requests/<int:request_id>/', views.answer_friend_request, name='request-detail'),
    path('friends/', views.FriendsListView.as_view(), name='friends'),

    
]
