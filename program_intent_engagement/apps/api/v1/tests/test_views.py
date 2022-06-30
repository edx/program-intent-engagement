"""
Tests for the program intent API views
"""
import json
import uuid

import ddt
from django.urls import reverse

from program_intent_engagement.apps.core.models import ProgramIntent
from test_utils import ProgramIntentsAPITestCase


@ddt.ddt
class ProgramIntentsViewTests(ProgramIntentsAPITestCase):
    """
    Tests Program Intents View
    """

    def setUp(self):
        super().setUp()

        self.url = reverse('api:v1:program_intent-insert')

        self.program_uuid = str(uuid.uuid4())
        self.data = {
            'program_uuid': self.program_uuid,
            'reason': 'ALL_COURSES_COMPLETE',
            'certainty': 'CERTAIN_YES',
            'effective_timestamp': '2022-07-01 00:00:00',
        }

    def post_api(self, user, data):
        """
        Helper function to make a POST request to the API
        """
        data = json.dumps(data)
        headers = self.build_jwt_headers(user)

        return self.client.post(self.url, data, **headers, content_type="application/json")

    def validate_response_code(self, user, data, expected_response_code):
        """
        Helper function to get API response and validate response code
        """
        response = self.post_api(user, data)
        self.assertEqual(response.status_code, expected_response_code)
        return response

    def test_auth_failures(self):
        """
        Test that the endpoint correctly validates permissions.
        """
        # test with anonymous user without jwt headers
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)

    def test_empty_program_intent(self):
        """
        Test that the endpoint returns 400 if input is empty
        """
        self.validate_response_code(self.user, {}, 400)

    def test_valid_program_intent(self):
        """
        Test that the endpoint returns 200 if input is valid
        """
        self.validate_response_code(self.user, self.data, 200)
        self.assertEqual(len(ProgramIntent.objects.all()), 1)
        intent = ProgramIntent.objects.get(program_uuid=self.program_uuid,
                                           reason='ALL_COURSES_COMPLETE',
                                           certainty='CERTAIN_YES',
                                           effective_timestamp='2022-07-01 00:00:00')
        self.assertIsNotNone(intent)

    def test_duplicate_program_intent(self):
        """
        Test that duplicate program intent returns 400 and that duplicate is not inserted
        """
        self.validate_response_code(self.user, self.data, 200)
        self.validate_response_code(self.user, self.data, 400)
        self.assertEqual(len(ProgramIntent.objects.all()), 1)

    def test_invalid_program_intent(self):
        """
        Test that endpoint returns 400 if input program intent does not pass serialization
        because reason field is missing.
        """
        data = {
            'program_uuid': self.program_uuid,
            'certainty': 'CERTAIN_YES',
            'effective_timestamp': '2022-07-01 00:00:00',
        }
        self.validate_response_code(self.user, data, 400)

    def test_invalid_certainty(self):
        """
        Test that endpoint returns 400 if program intent certainty is invalid
        """
        data = {
            'program_uuid': self.program_uuid,
            'reason': 'ALL_COURSES_COMPLETE',
            'certainty': 'YES',
            'effective_timestamp': '2022-07-01 00:00:00',
        }
        self.validate_response_code(self.user, data, 400)

    def test_unique_program_intents(self):
        """
        Test that similar program intents with distinct reason fields are both inserted and 200 is returned.
        """
        data_similar = {
            'program_uuid': self.program_uuid,
            'reason': 'BUNDLE_PURCHASE',
            'certainty': 'CERTAIN_YES',
            'effective_timestamp': '2022-07-01 00:00:00',
        }
        self.validate_response_code(self.user, self.data, 200)
        self.validate_response_code(self.user, data_similar, 200)
        self.assertEqual(len(ProgramIntent.objects.all()), 2)

    def test_distinct_effective_timestamp_program_intents(self):
        """
        Test that similar program intents with distinct effective timestamps are both inserted and 200 is returned.
        """
        data_similar = {
            'program_uuid': self.program_uuid,
            'reason': 'ALL_COURSES_COMPLETE',
            'certainty': 'CERTAIN_YES',
            'effective_timestamp': '2022-07-02 00:00:00',
        }
        self.validate_response_code(self.user, self.data, 200)
        self.validate_response_code(self.user, data_similar, 200)
        self.assertEqual(len(ProgramIntent.objects.all()), 2)
