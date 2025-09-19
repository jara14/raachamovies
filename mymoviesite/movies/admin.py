from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Movie, Booking, UserProfile

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'show_date', 'show_time', 'location', 'price')
    list_filter = ('category', 'show_date')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'movie', 'tickets', 'paid', 'status', 'created_at')
    list_filter = ('paid', 'status', 'created_at')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    fields = ('phone', 'address')

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    
    # Add phone to the list display
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_phone', 'is_staff')
    
    # Add phone to search fields
    search_fields = ('username', 'first_name', 'last_name', 'email', 'userprofile__phone')
    
    # Add a method to display phone in list view
    def get_phone(self, obj):
        try:
            return obj.userprofile.phone if obj.userprofile.phone else '-'
        except UserProfile.DoesNotExist:
            return '-'
    get_phone.short_description = 'Phone'
    get_phone.admin_order_field = 'userprofile__phone'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Unregister the default User admin
admin.site.unregister(User)
# Register the custom User admin
admin.site.register(User, CustomUserAdmin)