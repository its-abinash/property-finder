#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'property_finder.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

"""
IMPORTANT ==>> Replace the empty dict with the cred_dict that has been attached in email
"""
env_data = {}

if __name__ == '__main__':
    for env_key, env_val in env_data.items():
        os.environ[str(env_key)] = str(env_val)
    main()
