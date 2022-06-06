import time
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    help = 'check db connection before boot'

    def handle(self, *args, **kwargs):
        db_up = False
        self.stdout.write('Waiting for database...')


        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database ready!'))
            