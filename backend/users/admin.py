from django.contrib import admin

from users.models import CustomUser, Tag


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(CustomUser)
admin.site.register(Tag, TagAdmin)
