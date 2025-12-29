# DNDownbeats Backend

A Django REST API for managing music soundtracks, categories, and subcategories.

> **Note**: This is the backend API. For the complete application, you'll also need the frontend:  
> 🔗 [DNDownbeats Frontend](https://github.com/Elyeet9/dndownbeats-frontend)

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Database Setup](#4-database-setup)
  - [5. Create a Superuser](#5-create-a-superuser-optional)
  - [6. Create Media Directories](#6-create-media-directories)
- [Running the Development Server](#running-the-development-server)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
  - [CORS Settings](#cors-settings)
  - [Database](#database)
  - [Media Files](#media-files)
- [Common Commands](#common-commands)
- [Development Notes](#development-notes)
  - [Security Warning](#security-warning)
  - [Django Cleanup](#django-cleanup)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview

This is a Django-based backend application that provides RESTful APIs for managing all data for Dungeons and Downbeats:
- **Soundtracks**: Music tracks with metadata and thumbnails
- **Categories**: Top-level music categories with thumbnails
- **Subcategories**: Nested categories with thumbnails

## Prerequisites

Before setting up this project, ensure you have the following installed:

- **Python 3.8+** (preferably Python 3.10 or higher)
- **pip** (Python package installer)
- **virtualenv** or **venv** (for virtual environment)
- **Git** (for version control)

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd dndownbeats-backend
```

### 2. Create a Virtual Environment

**On Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses the following main dependencies:
- Django 5.1.7+
- Django REST Framework 3.15.2
- django-cors-headers 4.6.0
- django-cleanup 9.0.0
- Pillow 10.0.0+
- requests 2.31.0+
- beautifulsoup4 4.12.0+

### 4. Database Setup

Initialize the database by running migrations:

```bash
python manage.py migrate
```

This will create a SQLite database (`db.sqlite3`) with all necessary tables.

### 5. Create a Superuser (Optional)

To access the Django admin panel, create a superuser account:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin credentials.

### 6. Create Media Directories

The project stores uploaded files in the `media` directory. The structure should already exist, but if needed:

```bash
mkdir -p media/categories/thumbnails
mkdir -p media/soundtracks/thumbnails
mkdir -p media/subcategories/thumbnails
```

## Running the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

**On Windows**, you can also use:
```bash
runserver.bat
```

The API will be available at: `http://localhost:8000/`

## API Endpoints

The application provides RESTful API endpoints (exact routes depend on your URL configuration):

- `/admin/` - Django admin interface
- API endpoints for:
  - Categories
  - Subcategories
  - Soundtracks

## Project Structure

```
dndownbeats-backend/
├── dndownbeats/              # Main project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI configuration
│   └── utils/                # Shared utilities
│       ├── constants.py      # Project constants
│       └── models.py         # Base models
├── downbeats/                # Main application
│   ├── models/               # Database models
│   │   ├── category.py
│   │   ├── soundtrack.py
│   │   └── subcategory.py
│   ├── serializers/          # DRF serializers
│   │   └── category.py
│   ├── views/                # API views
│   │   ├── category.py
│   │   ├── soundtrack.py
│   │   └── subcategory.py
│   ├── migrations/           # Database migrations
│   └── admin.py              # Admin configuration
├── media/                    # Uploaded files
│   ├── categories/
│   ├── soundtracks/
│   └── subcategories/
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Configuration

### CORS Settings

The project is configured to allow CORS requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

For development, `CORS_ALLOW_ALL_ORIGINS` is set to `True`.

### Database

The project uses SQLite by default. To switch to PostgreSQL or MySQL, update the `DATABASES` setting in [dndownbeats/settings.py](dndownbeats/settings.py).

### Media Files

Uploaded files are stored in the `media/` directory. The `MEDIA_URL` is set to `/media/` and `MEDIA_ROOT` points to the `media/` folder in the project root.

## Common Commands

### Create New App
```bash
python manage.py startapp app_name
```

### Make Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Run Shell
```bash
python manage.py shell
```

### Collect Static Files
```bash
python manage.py collectstatic
```

## Development Notes

### Security Warning

⚠️ **Important**: The current `SECRET_KEY` in settings.py is for development only. Before deploying to production:

1. Generate a new secret key
2. Move it to environment variables
3. Set `DEBUG = False`
4. Configure `ALLOWED_HOSTS` appropriately
5. Use a production-grade database (PostgreSQL, MySQL, etc.)

### Django Cleanup

The project uses `django-cleanup` to automatically delete old files when:
- A model instance with a FileField is deleted
- A FileField's value is changed

## Troubleshooting

### Virtual Environment Not Activating

If you have issues activating the virtual environment:
- Ensure you're in the project directory
- Check that Python is installed and accessible
- Try using `python` instead of `python3` or vice versa

### Missing Dependencies

If you encounter import errors:
```bash
pip install -r requirements.txt --upgrade
```

### Database Issues

To reset the database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Port Already in Use

If port 8000 is already in use, specify a different port:
```bash
python manage.py runserver 8080
```
