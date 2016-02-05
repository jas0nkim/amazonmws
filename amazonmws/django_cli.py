import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

###### setting django module ######

def execute():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rfi.settings")
    import django
    django.setup()

