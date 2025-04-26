from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Booking
from .forms import BookingForm
from django.conf import settings
from django.http import JsonResponse
import stripe
from django.contrib.auth.decorators import login_required
from .models import UserProfile


stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    now_showing = Movie.objects.filter(category='now_showing')
    upcoming = Movie.objects.filter(category='upcoming')
    return render(request, 'movies/home.html', {
        'now_showing': now_showing,
        'upcoming': upcoming,
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    bookings = Booking.objects.filter(movie=movie)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.movie = movie
            booking.save()
            return JsonResponse({'success': True, 'booking_id': booking.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    form = BookingForm()
    return render(request, 'movies/detail.html', {'movie': movie, 'form': form, 'bookings': bookings})



@login_required
def user_profile(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)  # Get all bookings for the logged-in user
    return render(request, 'movies/profile.html', {'user': user, 'bookings': bookings})


@login_required
def book_ticket(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.movie = movie
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            return redirect('pay', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'movies/book.html', {'form': form, 'movie': movie})


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not logged in
    user_profile = UserProfile.objects.get(user=request.user)
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'movies/profile.html', {'user_profile': user_profile, 'bookings': bookings})



def pay(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': booking.movie.price * 100 * booking.tickets,  # dynamic price!
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
