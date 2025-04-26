from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Booking, UserProfile
from .forms import BookingForm, CustomUserCreationForm
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

from .forms import BookingForm, CustomUserCreationForm, UserUpdateForm, UserProfileForm,CustomPasswordChangeForm



stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    movies = Movie.objects.all()
    query = request.GET.get('q')
    category = request.GET.get('category')
    if query:
        movies = movies.filter(title__icontains=query)
    if category:
        movies = movies.filter(category=category)
    return render(request, 'movies/home.html', {'movies': movies})


from django.urls import reverse

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = BookingForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            login_url = reverse('login') + f'?next=/movie/{pk}/'
            messages.error(request, 'You need to log in to book tickets.')
            return redirect(login_url)

        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.movie = movie
            booking.user = request.user
            booking.save()
            return redirect('pay', booking_id=booking.id)

    return render(request, 'movies/detail.html', {'movie': movie, 'form': form})



# views.py
def pay(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    # If the booking is already paid, redirect to the profile page
    if booking.paid:
        return redirect('profile')

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(booking.movie.price * 100) * booking.tickets,
                'product_data': {
                    'name': f'Tickets for {booking.movie.title}',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/') + f'?booking_id={booking.id}',
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    # Redirect the user to Stripe checkout
    return redirect(session.url, code=303)


def payment_success(request):
    booking_id = request.GET.get('booking_id')
    if booking_id:
        booking = Booking.objects.get(id=booking_id)
        booking.paid = True
        booking.status = 'Paid'  # Update the status to "Paid"
        booking.save()
    return render(request, 'movies/success.html')


def payment_cancel(request):
    return render(request, 'movies/cancel.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'movies/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'movies/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


def profile_view(request):
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, instance=profile)
            password_form = CustomPasswordChangeForm(request.user, request.POST)

            if 'update_profile' in request.POST:
                if user_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    profile_form.save()
                    messages.success(request, 'Profile updated successfully!')
                    return redirect('profile')

            elif 'change_password' in request.POST:
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)  # important to keep user logged in
                    messages.success(request, 'Password changed successfully!')
                    return redirect('profile')
                else:
                    messages.error(request, 'Please correct the errors below.')

        else:
            # Pre-fill the forms with existing data
            user_form = UserUpdateForm(instance=request.user)
            profile_form = UserProfileForm(instance=profile)
            password_form = CustomPasswordChangeForm(request.user)

        bookings = Booking.objects.filter(user=request.user)

        return render(request, 'movies/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form,
            'bookings': bookings,
        })
    else:
        return redirect('login')

