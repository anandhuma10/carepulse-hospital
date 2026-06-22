import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings') # Replace with your project folder name
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
# Change these values to your preferred login info
username = 'admin'
email = 'admin@carepulse.com'
password = 'YourSecurePassword123!' 

if not User.objects.filter(username=username).exists():
    print("Creating superuser...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
