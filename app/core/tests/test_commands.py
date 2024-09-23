"""
Test custom django management commands.
"""

from unittest.mock import patch   # simulating DB behaviour

# Exception throwed while connecting to DB before its ready
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """ test commands """

    def test_wait_for_db_ready(self, patched_check):
        """ Test waiting for DB if DB ready """
        patched_check.return_value = True
        call_command('wait_for_db')   # python manage.py wait_for_db

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Test wating for DB when getting OperationalError """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        # Mocking the sleep fn, so that it returns None everytime when called
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
