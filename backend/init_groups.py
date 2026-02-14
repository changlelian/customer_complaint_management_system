import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group

groups = ['普通用户', '现场用户', '审核用户', '管理员']

for name in groups:
    group, created = Group.objects.get_or_create(name=name)
    if created:
        print(f"Group '{name}' created.")
    else:
        print(f"Group '{name}' already exists.")
