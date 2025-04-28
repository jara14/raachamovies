**README.md**

# 🎬 Django Movie Booking Website

A Django web application to browse movies, select seats, book tickets, and pay securely using Stripe. It features user profiles, seat selection, category search, and mobile responsiveness.

---

## ✨ Features

- Browse movies, filter by category or search
- Movie detail page with seat selection
- Book multiple tickets with secure Stripe payment
- User authentication (Sign Up / Login / Logout)
- Update profile (name, email, phone, address, password)
- View past bookings
- Smooth UX with flash messages

---

## 🛠️ Tech Stack

- Backend: Django 5.x
- Frontend: HTML, CSS, Bootstrap 5
- Payments: Stripe Checkout
- Database: SQLite (easy to switch to PostgreSQL)

---

## 📂 Project Structure

```
mymoviesite/
├── movies/
│   ├── templates/
│   │   ├── movies/
│   │       ├── base.html, home.html, detail.html, signup.html, login.html, profile.html, success.html, cancel.html
│   ├── static/
│   ├── admin.py, apps.py, forms.py, models.py, urls.py, views.py
├── media/
├── manage.py
└── mymoviesite/
    ├── settings.py, urls.py, wsgi.py
```

---

## 🚀 Installation Guide

1. Clone repository
```bash
git clone https://github.com/your-username/django-movie-booking.git
cd django-movie-booking
```

2. Create and activate virtual environment
```bash
python -m venv env
source env/bin/activate  # For Linux/Mac
# OR
env\Scripts\activate    # For Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup database
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create admin user
```bash
python manage.py createsuperuser
```

6. Add Stripe keys in `settings.py`
```python
STRIPE_SECRET_KEY = 'your_stripe_secret_key'
STRIPE_PUBLISHABLE_KEY = 'your_stripe_publishable_key'
```

7. Run development server
```bash
python manage.py runserver
```
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🎟️ Booking Flow

- Choose a movie
- Select available seats
- Book tickets
- Pay securely via Stripe Checkout
- Seats are reserved after payment success

---

## 👨‍💻 Author

**Your Name**  
GitHub: [@jara14](https://github.com/jara14)  
LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/jayakrishnaraavi/)

---

**requirements.txt**

```
django>=5.0
stripe>=8.0
```

*(If you used Bootstrap locally, no extra package needed; if using "whitenoise" for deployment, it can be added later.)*

---

Would you also like me to add a short "How Seat Selection Works" section in README too? (Optional Bonus! 🚀)
