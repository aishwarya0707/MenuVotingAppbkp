from django.contrib import admin

# Register your models here.
from .models import Restaurant, Menu, Vote

# Register your models here.

# Register your models here.
# admin.site.register(Restaurant)
# admin.site.register(Menu)


class RestaurantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "cuisine_type",
        "phone_number",
        "address",
        "opening_hours",
    )


class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "items", "votes", "date")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("menu", "points", "employee", "voted_date")
    list_filter = ("menu", "employee", "voted_date")
    search_fields = ("menu__restaurant__name", "employee__username")
    readonly_fields = ("menu", "points", "employee", "voted_date")
    date_hierarchy = "voted_date"
    ordering = ("-voted_date",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)