from django.contrib import admin
from .models import Movie, Booking, UserProfile


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'show_date', 'show_time', 'location', 'price')
    list_filter = ('category', 'show_date')

admin.site.register(UserProfile)
admin.site.register(Booking)