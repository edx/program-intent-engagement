"""
Command to create program intents
"""

import csv
import logging
import time

from django.core.management import BaseCommand

from program_intent_engagement.apps.core.models import ProgramIntent

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Command to add program intents defined in a csv file
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch_size',
            action='store',
            dest='batch_size',
            type=int,
            default=500,
            help='Maximum number of intents to process. '
                 'This helps avoid overloading the database while updating large amount of data.'
        )
        parser.add_argument(
            '--sleep_time',
            action='store',
            dest='sleep_time',
            type=int,
            default=10,
            help='Sleep time in seconds between update of batches'
        )

        parser.add_argument(
            '--csv_filepath',
            action='store',
            dest='csv_filepath',
            type=str,
            help='Filepath for CSV containing program intent data'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        sleep_time = options['sleep_time']
        csv_filepath = options['csv_filepath']

        with open(csv_filepath, 'r') as csv_file:
            intents = []
            lines = csv.DictReader(csv_file)
            for line in lines:
                program_uuid = line['PROGRAM_UUID']
                lms_user_id = line['USER_ID']
                reason = line['INTENT_REASON']
                certainty = line['INTENT_CERTAINTY']
                # remove ' Z' from timestamp, because Django does not accept format
                # and there is no timezone data
                effective_timestamp = line['EFFECTIVE_TIME'][:-2]

                existing_intent = ProgramIntent.objects.filter(
                    program_uuid=program_uuid,
                    lms_user_id=lms_user_id,
                    reason=reason,
                    certainty=certainty,
                    effective_timestamp=effective_timestamp
                ).first()

                if not existing_intent:
                    new_intent = ProgramIntent(
                        program_uuid=program_uuid,
                        lms_user_id=lms_user_id,
                        reason=reason,
                        certainty=certainty,
                        effective_timestamp=effective_timestamp
                    )
                    intents.append(new_intent)
                    log.info('Adding intent=%(intent_id)s to batch', {'intent_id': new_intent.id})

                if len(intents) == batch_size:
                    log.info('Creating %(batch_size) intents', {'batch_size': batch_size})
                    ProgramIntent.objects.bulk_create(intents)
                    intents = []

                    log.info('Sleeping for %(sleep_time) seconds', {'sleep_time': sleep_time})
                    time.sleep(sleep_time)

            if intents:
                log.info('Creating remaining %(num) intents', {'num': len(intents)})
                ProgramIntent.objects.bulk_create(intents)
