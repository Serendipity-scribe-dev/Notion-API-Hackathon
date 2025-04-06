from django.contrib import admin

# Register your models here.

from .models import MemberProfile,NotionConfig

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'notion_page_id', 'submitted_at')


admin.site.register(NotionConfig)
