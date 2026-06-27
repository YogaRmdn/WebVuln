import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulnapp.settings')
django.setup()

from django.contrib.auth.models import User
from lab.models import BlogPost, Comment, Product, ProtectedDocument


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

    # Create protected documents
    if not ProtectedDocument.objects.exists():
        docs = [
            ProtectedDocument(
                title='Internal Network Map',
                content='192.168.1.0/24 — Office LAN\n10.0.0.0/8 — Internal Infrastructure\n172.16.0.0/12 — DMZ\n\nDNS Servers:\n  - 10.0.0.53 (Internal DNS)\n  - 8.8.8.8 (External Forwarder)\n\nDomain Controllers:\n  - DC01 (10.0.0.10)\n  - DC02 (10.0.0.11)',
                category='Infrastructure',
                required_role='admin',
            ),
            ProtectedDocument(
                title='Database Credentials',
                content='PostgreSQL Master Database\n  Host: db01.internal\n  Port: 5432\n  Database: prod_app\n  Username: db_admin\n  Password: S3cur3P@ssw0rd!\n\nRedis Cache\n  Host: redis01.internal\n  Port: 6379\n  Password: r3d1s_c4ch3_k3y',
                category='Secrets',
                required_role='admin',
            ),
            ProtectedDocument(
                title='Employee Salary Records',
                content='ID | Name | Position | Salary\n----------------------------------------\n001 | Admin User | CEO | $250,000\n002 | Alice Smith | Developer | $120,000\n003 | Bob Jones | Developer | $115,000\n004 | Charlie Brown | Security | $145,000\n005 | Diana Prince | DevOps | $130,000',
                category='HR',
                required_role='hr_admin',
            ),
            ProtectedDocument(
                title='Incident Response Runbook',
                content='== PHASE 1: IDENTIFICATION ==\n1. Monitor SIEM alerts\n2. Verify alert legitimacy\n3. Assign severity level\n\n== PHASE 2: CONTAINMENT ==\n1. Isolate affected systems\n2. Block malicious IPs\n3. Preserve forensic evidence\n\n== PHASE 3: ERADICATION ==\n1. Remove malware\n2. Patch vulnerabilities\n3. Rotate compromised credentials\n\n== PHASE 4: RECOVERY ==\n1. Restore from clean backups\n2. Monitor for re-infection\n3. Return to normal operations',
                category='Security',
                required_role='admin',
            ),
        ]
        ProtectedDocument.objects.bulk_create(docs)

    print('Seed data created successfully!')
    print(f'  - {User.objects.count()} users')
    print(f'  - {BlogPost.objects.count()} blog posts')
    print(f'  - {Product.objects.count()} products')
    print(f'  - {ProtectedDocument.objects.count()} protected documents')
    print()
    print('Users created:')
    print('  admin / admin123 (superuser)')
    print('  alice / password123')
    print('  bob / password456')


if __name__ == '__main__':
    seed()
