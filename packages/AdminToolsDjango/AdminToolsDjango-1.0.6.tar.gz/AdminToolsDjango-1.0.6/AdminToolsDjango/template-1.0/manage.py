#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os, sys
from admin_script import *


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) >= 2 and sys.argv[1] in ls_my_cmd:
        eval(sys.argv[1])
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

