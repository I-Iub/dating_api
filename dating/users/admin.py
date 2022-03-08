from django.contrib import admin

from users.models import Match, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'gender', 'email')
    search_field = ('username', 'email')
    list_filter = ('gender',)
    empty_value_display = '<пусто>'


class MatchAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'candidate', 'like')
    search_field = ('user', 'candidate')
    list_filter = ('like',)
    empty_value_display = '<пусто>'


admin.site.register(User, UserAdmin)
admin.site.register(Match, MatchAdmin)
