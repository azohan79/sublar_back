from django.contrib import admin
from .models import User, MenuItem, PortalSettings, MarketingPlan

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'phone', 'partner_type', 'is_active', 'is_staff', 'avatar']
    search_fields = ['email', 'full_name']

admin.site.register(User, UserAdmin)
admin.site.register(MenuItem)

@admin.register(PortalSettings)
class PortalSettingsAdmin(admin.ModelAdmin):
    list_display = ('header_logo',)
    filter_horizontal = ('header_menu', 'footer_menu',)

@admin.register(MarketingPlan)
class MarketingPlanAdmin(admin.ModelAdmin):
    list_display = ('partner_types', 'qualification_types', 'activity_period',)
