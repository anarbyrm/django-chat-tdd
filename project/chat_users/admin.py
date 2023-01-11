from django.contrib import admin

from chat_users.models import User, FriendRequest


admin.site.register(User)
admin.site.register(FriendRequest)
