import subprocess
import os
import sqlite3

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from .models import BlogPost, Comment, Product, UploadedFile, ProtectedDocument
from .forms import CommentForm, SearchForm, UploadForm, FeedbackForm, TransferForm


def index(request):
    posts = BlogPost.objects.all()
    return render(request, 'lab/index.html', {'posts': posts})


# -- SQL Injection --

def sqli_login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        with connection.cursor() as cursor:
            query = f"SELECT * FROM auth_user WHERE username='{username}' AND password='{password}'"
            cursor.execute(query)
            user_row = cursor.fetchone()
        if user_row:
            return HttpResponse("Login successful! Welcome, " + username)
        else:
            error = 'Invalid credentials'
    return render(request, 'lab/sqli_login.html', {'error': error})


def sqli_search(request):
    results = []
    query = ''
    error = ''
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if query:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(f"SELECT id, username, email FROM auth_user WHERE username LIKE '%{query}%'")
                    results = cursor.fetchall()
                except Exception as e:
                    error = str(e)
    return render(request, 'lab/sqli_search.html', {'results': results, 'query': query, 'error': error})


def sqli_product(request):
    products = []
    cat = request.GET.get('cat', '')
    if cat:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM lab_product WHERE category='{cat}'")
            products = cursor.fetchall()
    return render(request, 'lab/sqli_product.html', {'products': products, 'cat': cat})


# -- XSS --

def xss_reflected(request):
    message = request.GET.get('msg', '')
    return render(request, 'lab/xss_reflected.html', {'message': message})


def xss_stored(request, post_id=None):
    if post_id:
        post = get_object_or_404(BlogPost, id=post_id)
    else:
        post = BlogPost.objects.first()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                post=post,
                author_name=form.cleaned_data['author_name'],
                content=form.cleaned_data['content'],
            )
            comment.save()
            return redirect('xss_stored', post_id=post.id)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(post=post)
    posts = BlogPost.objects.all()
    return render(request, 'lab/xss_stored.html', {
        'post': post, 'posts': posts,
        'comments': comments, 'form': form,
    })


def xss_dom(request):
    return render(request, 'lab/xss_dom.html')


# -- File Upload --

def upload_file(request):
    uploaded = None
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uf = UploadedFile.objects.create(
                file=request.FILES['file'],
                description=form.cleaned_data.get('description', ''),
            )
            uploaded = uf
    else:
        form = UploadForm()
    files = UploadedFile.objects.all().order_by('-uploaded_at')
    return render(request, 'lab/upload.html', {'form': form, 'uploaded': uploaded, 'files': files})


# -- Command Injection --

def cmd_injection(request):
    output = ''
    command = ''
    if request.method == 'POST':
        command = request.POST.get('target', '')
        if command:
            try:
                result = subprocess.run(
                    f'ping -c 1 {command}',
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                output = result.stdout + result.stderr
            except subprocess.TimeoutExpired:
                output = 'Command timed out.'
            except Exception as e:
                output = f'Error: {e}'
    return render(request, 'lab/cmd_injection.html', {'output': output, 'command': command})


# -- Path Traversal --

def path_traversal(request):
    content = ''
    filename = request.GET.get('file', '')
    if filename:
        safe_dir = os.path.join(settings.BASE_DIR, 'lab', 'files')
        filepath = os.path.join(safe_dir, filename)
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except Exception as e:
            content = f'Error reading file: {e}'
    return render(request, 'lab/path_traversal.html', {'content': content, 'filename': filename})


# -- IDOR --

@login_required
def idor_profile(request, user_id):
    try:
        profile_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found")
    return render(request, 'lab/idor_profile.html', {'profile_user': profile_user})


@login_required
def idor_update_email(request, user_id):
    try:
        profile_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found")

    if request.method == 'POST':
        new_email = request.POST.get('email', '')
        profile_user.email = new_email
        profile_user.save()
        return redirect('idor_profile', user_id=user_id)
    return render(request, 'lab/idor_update_email.html', {'profile_user': profile_user})


# -- Open Redirect --

def open_redirect(request):
    url = request.GET.get('url', '')
    if url:
        return redirect(url)
    return render(request, 'lab/open_redirect.html')


# -- CSRF --

@csrf_exempt
def csrf_transfer(request):
    message = ''
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            message = f"Transferred ${form.cleaned_data['amount']} to account {form.cleaned_data['to_account']}"
    else:
        form = TransferForm()
    return render(request, 'lab/csrf_transfer.html', {'form': form, 'message': message})


# -- Feedback / Information Disclosure

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            message = f"Thanks for your feedback: {form.cleaned_data['message']}"
            return render(request, 'lab/feedback.html', {'form': FeedbackForm(), 'message': message})
    else:
        form = FeedbackForm()
    return render(request, 'lab/feedback.html', {'form': form})


def debug_info(request):
    import socket
    import platform
    info = {
        'hostname': socket.gethostname(),
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'django_settings': settings.DATABASES,
        'secret_key': settings.SECRET_KEY[:20] + '...',
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
    }
    return render(request, 'lab/debug_info.html', {'info': info})


def robots(request):
    content = "User-agent: *\nDisallow: /admin/\nDisallow: /debug/\n"
    return HttpResponse(content, content_type='text/plain')


def security_txt(request):
    content = "Contact: mailto:admin@example.com\nExpires: 2026-12-31\n"
    return HttpResponse(content, content_type='text/plain')


# -- 403 Forbidden Bypass --

def protected_index(request):
    bypassed = _check_403_bypass(request)
    if not bypassed:
        return HttpResponse('403 Forbidden — Access Denied', status=403)

    docs = ProtectedDocument.objects.all()
    categories = ProtectedDocument.objects.values_list('category', flat=True).distinct()
    return render(request, 'lab/protected.html', {
        'docs': docs,
        'categories': categories,
    })


def protected_document(request, doc_id):
    bypassed = _check_403_bypass(request)
    if not bypassed:
        return HttpResponse('403 Forbidden — Access Denied', status=403)

    doc = get_object_or_404(ProtectedDocument, id=doc_id)
    return render(request, 'lab/protected_detail.html', {'doc': doc})


def _check_403_bypass(request):
    if request.META.get('HTTP_X_ORIGINAL_URL'):
        return True
    if request.META.get('HTTP_X_REWRITE_URL'):
        return True
    if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
        return True
    if '..;/' in request.path:
        return True
    return False
