from django.contrib import admin
from .models import Note, New_Project, New_registration, Document_details, post_image, PostImage, PlotAvailability, PlotAmount
# Register your models here.

admin.site.register(Note)
admin.site.register(New_Project)
admin.site.register(New_registration)
admin.site.register(Document_details)
admin.site.register(post_image)
admin.site.register(PostImage)
admin.site.register(PlotAvailability)
# admin.site.register(PlotAmount)