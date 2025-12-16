
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from api.models import Result

def clear_data():
    count = Result.objects.all().count()
    Result.objects.all().delete()
    print(f"Deleted {count} test results.")

if __name__ == '__main__':
    clear_data()
