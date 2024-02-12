from django.contrib import admin
from .models import Game


# admin.site.register(Game)


@admin.register(Game)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'width', 'height', 'mines_count', 'completed', 'field')
    fields = ('game_id', 'width', 'height', 'mines_count', 'completed', 'field')

    readonly_fields = ('game_id', 'completed', 'field')
