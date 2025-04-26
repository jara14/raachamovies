from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/', views.profile, name='profile'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:pk>/book/', views.book_ticket, name='book_ticket'),
    path('pay/<int:booking_id>/', views.pay, name='pay'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),

]
