"""
Django command to wait for the database to be available.
"""

import time
from psycopg2 import OperationalError as Psycop2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    waits for DB to be ready before running application
    """

    def handle(self, *args, **kwargs):
        """Entry point for the cmd"""
        self.stdout.write('waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycop2Error, OperationalError):
                self.stdout.write('DB unavailable, waiting for 2 second...')
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS('DB available!'))
