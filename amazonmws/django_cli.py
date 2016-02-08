import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rfi'))

from django.core.exceptions import AppRegistryNotReady

###### setting django module ######

def execute():
    try:
        from django.apps import apps
        apps.check_apps_ready()

    except AppRegistryNotReady:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rfi.cli_settings")
        import django
        django.setup()

