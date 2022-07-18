""" Tests for bulk_insert_intents management command """
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from program_intent_engagement.apps.core.models import ProgramIntent


class BulkInsertIntentsTests(TestCase):
    """ Test bulk_insert_intents management command """

    def test_create_intents(self):
        """
        Test that intents are created from csv file
        """
        call_command(
            'bulk_insert_intents',
            batch_size=2,
            sleep_time=0,
            csv_filepath=str(Path(__file__).parent / 'fixtures_data' / 'test_intents.csv')
        )

        # assert that three objects have been created
        intents = ProgramIntent.objects.all()
        self.assertEqual(len(intents), 3)

    def test_no_duplicate_intents(self):
        """
        Test that an intent is not duplicated
        """
        # add program intent with same data as row in csv file
        existing_intent = ProgramIntent.objects.create(
            program_uuid='599e9ab206a211edb9390242ac120002',
            lms_user_id=1,
            reason='ENROLLED_ALL_COURSES',
            certainty='MAYBE',
            effective_timestamp='2020-11-24 12:00:00'
        )

        call_command(
            'bulk_insert_intents',
            batch_size=2,
            sleep_time=0,
            csv_filepath=str(Path(__file__).parent / 'fixtures_data' / 'test_intents.csv')
        )

        # assert that only 3 intents exist, with only one with the same intent reason
        intents = ProgramIntent.objects.all()
        self.assertEqual(len(intents), 3)

        duplicate_intent = ProgramIntent.objects.filter(
            program_uuid=existing_intent.program_uuid,
            lms_user_id=existing_intent.lms_user_id,
            reason=existing_intent.reason,
            certainty=existing_intent.certainty,
            effective_timestamp=existing_intent.effective_timestamp
        )
        self.assertEqual(len(duplicate_intent), 1)
