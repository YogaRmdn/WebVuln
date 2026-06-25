# WebVuln

**WebVuln** is a deliberately vulnerable Django web application designed for cybersecurity training and penetration testing practice. It provides a safe, legal environment to learn and practice exploiting common web vulnerabilities across multiple categories.

> **Warning:** This application contains intentional security flaws. Do **not** deploy it in a production environment or expose it to the public internet.

---

## Features

WebVuln includes **10+ vulnerability categories** with multiple scenarios per category:

| Category | Endpoints | Description |
|----------|-----------|-------------|
| **SQL Injection** | `/sqli/login/`, `/sqli/search/`, `/sqli/product/` | Classic SQLi in login bypass, search fields, and product listing |
| **XSS (Reflected)** | `/xss/reflected/` | Reflected cross-site scripting via URL parameters |
| **XSS (Stored)** | `/xss/stored/` | Persistent XSS via blog post comments |
| **XSS (DOM-based)** | `/xss/dom/` | Client-side DOM-based XSS |
| **Command Injection** | `/cmd/` | OS command injection via `ping` parameter |
| **Path Traversal** | `/file/` | Directory traversal via file retrieval endpoint |
| **File Upload** | `/upload/` | Unrestricted file upload with no validation |
| **IDOR** | `/profile/<id>/` | Insecure Direct Object Reference on user profiles |
| **CSRF** | `/transfer/` | Missing CSRF protection on fund transfer |
| **Open Redirect** | `/redirect/` | Unvalidated redirect via `url` parameter |
| **Information Disclosure** | `/debug/`, `/robots.txt`, `/.well-known/security.txt` | Debug endpoint exposing configuration and secrets |

---

## Tech Stack

- **Backend:** Python 3 + Django
- **Database:** SQLite (default)
- **Templates:** Django Template Engine
- **Static Files:** Built-in Django static file serving

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YogaRmdn/WebVuln.git
cd WebVuln

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Seed sample data (users, blog posts, products)
python seed.py

# Start the development server
python manage.py runserver
```

The application will be available at **http://127.0.0.1:8000**.

### Quick Run

```bash
chmod +x run.sh && ./run.sh
```

### Default Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Superuser |
| `alice` | `password123` | Regular user |
| `bob` | `password456` | Regular user |

---

## Lab Scenarios

### SQL Injection
- **Login Bypass:** Enter `' OR '1'='1` as the username with any password
- **Search:** Try `' UNION SELECT id, username, password FROM auth_user --` in the search bar
- **Product Listing:** Manipulate the `cat` parameter to extract arbitrary data

### Cross-Site Scripting (XSS)
- **Reflected:** Pass `<script>alert('XSS')</script>` via the `msg` parameter
- **Stored:** Submit JavaScript payloads in blog post comments
- **DOM-based:** Exploit client-side DOM manipulation to execute scripts

### Command Injection
- **Ping Feature:** Append shell commands after the target IP, e.g., `127.0.0.1; id`
- **Path Traversal:** Use `../` sequences to read files outside the intended directory

### IDOR
- Access other users' profiles by changing the `user_id` parameter in the URL
- Update another user's email address without authorization

### CSRF
- The `/transfer/` endpoint processes state-changing requests without CSRF tokens
- Craft a malicious page that submits the transfer form on behalf of an authenticated user

---

## Project Structure

```
WebVuln/
├── lab/                    # Main application with vulnerable endpoints
│   ├── files/              # Sample files for path traversal lab
│   ├── migrations/         # Django database migrations
│   ├── templates/          # HTML templates
│   ├── admin.py            # Admin configuration
│   ├── forms.py            # Form definitions
│   ├── models.py           # Database models (BlogPost, Comment, Product, UploadedFile)
│   ├── urls.py             # URL routing for all lab endpoints
│   └── views.py            # View logic with intentional vulnerabilities
├── vulnapp/                # Django project configuration
│   ├── settings.py         # Project settings (DEBUG=True, no CSRF middleware)
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI application entry point
├── static/                 # Static assets (CSS, JS)
├── media/                  # Uploaded files directory
├── manage.py               # Django management script
├── seed.py                 # Database seeder with sample data
├── run.sh                  # Quick setup and run script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Security Notes

WebVuln is an **educational tool** intended for:

- Security researchers and ethical hackers
- Students learning web application security
- CTF (Capture The Flag) participants
- Developers wanting to understand vulnerabilities

**Do not** use this application:
- As a production website
- On a public-facing server
- For illegal or unauthorized testing

The vulnerabilities in this application are deliberately simplified for learning purposes and may not reflect real-world exploitation complexity.

---

## License

This project is provided for educational purposes only.
