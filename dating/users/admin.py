from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'gender', 'email')
    search_field = ('username', 'email')
    list_filter = ('gender',)
    empty_value_display = '<пусто>'


admin.site.register(User, UserAdmin)
