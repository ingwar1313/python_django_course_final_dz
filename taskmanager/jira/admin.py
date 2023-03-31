from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.

from .models import Tasks, Users, Projects, Sprints

class UsersAdmin(UserAdmin):
    # pass
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Fields',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'role',
                    'dept'
                ),
            },
        ),
    )

admin.site.register(Users, UsersAdmin)
admin.site.register(Tasks)
admin.site.register(Projects)
admin.site.register(Sprints)

