# Linktastic

## Description

This is a website made in Django that allows users to shorten URL's and create a hub for any
personal links which they can then share with anyone. The website is currently hosted at https://link-tastic.com.
This website allows users to take any URL and have it shortened using base 62 encoding. It allows users
to customize their profile and the format of their links to change the way it looks for other people. 

This website is being hosted using GCP App Engine. It uses a Google Cloud PostgreSQL database and a bucket for
static and media files.

Note: Webflow.com was partially used for the front end, hence the majority of the code is being registered as CSS.

## Installation

### Prerequisites
- Python
- PostgreSQL
- GCP setup and configuration (if using GCP for production)

### Steps
1. Clone the repository: `git clone https://github.com/rgg1/linktastic.git`
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4. Install required packages: `pip install -r requirements.txt`
5. Apply database migrations: `python manage.py migrate`
6. Run the server: `python manage.py runserver`

## Local Configuration Guide

To run this project locally or in your own production environment, you'll need to make some changes to the `settings.py` file:

### 1. **Django Secret Key**:
   - Generate a new secret key for Django. You can use [Django's Secret Key Generator](https://djecrety.ir/) or another tool.
   - Add it as an environment variable named `'SECRET_KEY'`, or modify `SECRET_KEY` in `settings.py` directly.

### 2. **Database Configuration**:
   - Set up a local PostgreSQL database, or configure a remote one.
   - Add environment variables for the database connection, including:
      - `'DJANGO_DB_NAME'`: Database name
      - `'DJANGO_DB_USER'`: Database user
      - `'DJANGO_DB_PASSWORD'`: Database password
      - `'DJANGO_DB_HOST'`: Database host
      - `'DJANGO_DB_PORT'`: Database port
   - Alternatively, you can modify the `DATABASES` dictionary in `settings.py` directly.
   - You could also use the default sqlite database with DEBUG mode turned on.

### 3. **AWS Configuration (if not in DEBUG mode)**:
   - If running in production (`DEBUG = False`), configure GCP for static and media file storage.
   - Modify the bucket name to your own bucket name.
   - Ensure appropriate GCP credentials and permissions are set up.

### 4. **Allowed Hosts**:
   - Update the `ALLOWED_HOSTS` list with your domain name, IP address, or other hosts as needed.

By configuring these settings, you should be able to run the project in a local or custom production environment.

Note that the GCP configuration is required for production deployments, so if you're not planning to use GCP, you would need to make further changes to how static and media files are served.

## Usage

This section provides a general guide on how to navigate and interact with PhotoVerse.

### Logging In
1. Visit the page at [Linktastic](https://link-tastic.com).
2. Register with a username and password or login if you've already made an account

### Adding/Removing Links
1. Go to the "Your Links" page if not there already.
2. Add a title and the url for a link and click on "Add Link".
3. Your links will appear to the right. Pressing the trash emoji will delete the link from your profile.

### Shortening URLs
1. Go to the "URL Shortener" page.
2. Enter any valid URL and press on "Shorten"
3. It will return to you a shortened URL that redirects to the input URL.

### Sharing Links Page
1. At the top of the home page click on "View your public profile".
2. This page shows what others will see when looking at your page. 
3. Simply share this URL so that anyone can see your personal links.

### Editing Your Profile or Link Format
1. Go to the "Settings" page.
2. Click on "Customize Link Formats" to change some options about what your links will look like.
3. Clicking on "Customize public profile picture, display name, and bio" will allow you to change these
other parts of your public profile. Photos support JPG and PNG.
