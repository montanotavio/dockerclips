import time

from psycopg2 import OperationalError as PsycopgError
from django.db.utils import OperationalError as UtilsError

from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting on database')
        db_ready = False
        while db_ready is False:
            try: 
                self.check(databases=['default'])
                db_ready = True
            except (PsycopgError, UtilsError):
                self.stdout.write('Waiting on database, checking again in 1 second')
                time.sleep(1)
        
        self.stdout.write('Database ready')
