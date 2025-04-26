from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Booking, UserProfile
from .forms import BookingForm, CustomUserCreationForm
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import stripe

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

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.movie = movie
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            return redirect('pay', booking_id=booking.id)
    return render(request, 'movies/detail.html', {'movie': movie, 'form': form})

def book_ticket(request, pk):
    return redirect('movie_detail', pk=pk)

def pay(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
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
    return redirect(session.url, code=303)

def payment_success(request):
    booking_id = request.GET.get('booking_id')
    if booking_id:
        booking = Booking.objects.get(id=booking_id)
        booking.paid = True
        booking.save()
    return render(request, 'movies/success.html')

def payment_cancel(request):
    return render(request, 'movies/cancel.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)  # ✅ this line ensures profile creation
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
        UserProfile.objects.get_or_create(user=request.user)  # ensure profile exists
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'movies/profile.html', {'bookings': bookings})
