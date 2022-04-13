#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from sound.sound import Sound
import webbrowser
import getpass

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def rickroll():
    if getpass.getuser() != 'BAPEHNKK': # check user name on windows
        Sound.volume_max()  # set max volume
        webbrowser.open_new_tab('https://youtu.be/dQw4w9WgXcQ') # DO IT !


if __name__ == '__main__':
    # rickroll()
    main()
