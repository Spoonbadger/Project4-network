from django.contrib import admin

# Register your models here.
from .models import User, Post, Like


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', ]
    filter_horizontal = ['following', ]


admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Like)
