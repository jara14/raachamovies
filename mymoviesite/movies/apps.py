from django.apps import AppConfig

class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'



class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    def ready(self):
        from django.contrib.auth.models import User
        from .models import UserProfile

        def get_user_profile(self):
            profile, created = UserProfile.objects.get_or_create(user=self)
            return profile

        User.add_to_class('profile', property(get_user_profile))
