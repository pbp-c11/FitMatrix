# FitMatrix

FitMatrix is a Django 5 application for managing fitness places, trainers, and personalized scheduling. The project ships with a glasmorphism-inspired interface and role-based dashboards for members and administrators.

## Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Seed demo data (optional but recommended):

```bash
python manage.py seed_demo
```

4. Run the development server:

```bash
python manage.py runserver
```

## Demo accounts

* **Admin** – `admin@fitmatrix.test` / `Admin123!`
* **Members** – `budi@fitmatrix.test`, `sri@fitmatrix.test`, `andika@fitmatrix.test`, `ayu@fitmatrix.test`, `rudi@fitmatrix.test`, `intan@fitmatrix.test`, `dimas@fitmatrix.test`, `melati@fitmatrix.test` (all use password `User12345!`).

## Routes overview

| Path | Description |
| --- | --- |
| `/` | Landing page |
| `/accounts/register/` | Member registration |
| `/accounts/login/` | Email/username login |
| `/accounts/profile/` | Profile dashboard with account, security, history, and wishlist tabs |
| `/accounts/profile/edit/` | Edit profile details |
| `/accounts/password/` | Change password |
| `/accounts/history/` | Paginated activity log |
| `/accounts/wishlist/` | Wishlist overview |
| `/accounts/wishlist/toggle/<kind>/<pk>/` | Add/remove wishlist items (AJAX) |
| `/places/` | Browse places |
| `/scheduling/` | Upcoming sessions |
| `/reviews/` | Member reviews |
| `/admin/console/` | Admin dashboard (role ADMIN) |
| `/admin/slots/` | Manage session slots |
| `/admin/bookings/` | View and cancel bookings |
| `/admin/reviews/` | Moderate reviews |
| `/django-admin/` | Django admin console |

## Media

User avatars are stored in `/media/avatars/`. Demo seed data also references placeholder SVG avatars stored under `accounts/static/demo/avatars/` (kept text-based for easy diffs and to avoid binary blobs in the repo).

## Testing

Run the automated test suite with:

```bash
python manage.py test
```
