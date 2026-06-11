import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulnapp.settings')
django.setup()

from django.contrib.auth.models import User
from lab.models import BlogPost, Comment, Product


def seed():
    # Create users
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin.first_name = 'Admin'
        admin.last_name = 'User'
        admin.save()
    else:
        admin = User.objects.get(username='admin')

    if not User.objects.filter(username='alice').exists():
        alice = User.objects.create_user('alice', 'alice@example.com', 'password123')
        alice.first_name = 'Alice'
        alice.last_name = 'Smith'
        alice.save()
    else:
        alice = User.objects.get(username='alice')

    if not User.objects.filter(username='bob').exists():
        bob = User.objects.create_user('bob', 'bob@example.com', 'password456')
        bob.first_name = 'Bob'
        bob.last_name = 'Jones'
        bob.save()
    else:
        bob = User.objects.get(username='bob')

    # Create blog posts
    if not BlogPost.objects.exists():
        posts = [
            BlogPost(title='Welcome to WebVuln Lab', content='This is a deliberately vulnerable Django application for practicing web security testing. Feel free to explore and find vulnerabilities.', author=admin),
            BlogPost(title='How to Test SQL Injection', content='SQL injection occurs when user input is directly concatenated into SQL queries. Try the login and search features to practice.', author=alice),
            BlogPost(title='Understanding XSS', content='Cross-Site Scripting (XSS) allows attackers to inject client-side scripts into web pages. Try the reflected, stored, and DOM-based XSS labs.', author=bob),
            BlogPost(title='Security Best Practices', content='Always validate and sanitize user input, use parameterized queries, implement CSRF tokens, and never trust client-side data.', author=admin),
        ]
        BlogPost.objects.bulk_create(posts)

    # Create products
    if not Product.objects.exists():
        products = [
            Product(name='Laptop', description='High-performance laptop', price=999.99, category='Electronics'),
            Product(name='Smartphone', description='Latest smartphone', price=699.99, category='Electronics'),
            Product(name='Coffee Mug', description='Ceramic coffee mug', price=12.99, category='Home'),
            Product(name='Desk Chair', description='Ergonomic desk chair', price=199.99, category='Furniture'),
            Product(name='Keyboard', description='Mechanical keyboard', price=89.99, category='Electronics'),
            Product(name='Notebook', description='Lined notebook', price=4.99, category='Stationery'),
            Product(name='Backpack', description='Travel backpack', price=49.99, category='Accessories'),
            Product(name='Headphones', description='Noise-cancelling headphones', price=149.99, category='Electronics'),
        ]
        Product.objects.bulk_create(products)

    print('Seed data created successfully!')
    print(f'  - {User.objects.count()} users')
    print(f'  - {BlogPost.objects.count()} blog posts')
    print(f'  - {Product.objects.count()} products')
    print()
    print('Users created:')
    print('  admin / admin123 (superuser)')
    print('  alice / password123')
    print('  bob / password456')


if __name__ == '__main__':
    seed()
