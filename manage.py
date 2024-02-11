#!/usr/bin/env python
import os, sys

"""
IMPORTANT ==>> Replace the empty dict with the cred_dict that has been attached in email
"""
env_data = {}

if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    for env_key, env_val in env_data.items():
        os.environ[str(env_key)] = str(env_val)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'property_finder.settings')
    execute_from_command_line(sys.argv)
