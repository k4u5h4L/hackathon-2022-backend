from django.contrib import admin

# Register your models here.


# admin stuff
name = "Dr Jadoo"
admin.site.site_header = f"{name} Admin"
admin.site.site_title = f"{name} Admin Portal"
admin.site.index_title = f"Welcome to {name} Portal"
