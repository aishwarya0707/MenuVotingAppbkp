from django.contrib import admin
from .models import Menu, Restaurant, Vote

class RestaurantAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "cuisine_type", "phone_number", "address")


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


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
