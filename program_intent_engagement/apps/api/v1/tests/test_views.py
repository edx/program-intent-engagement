"""
Tests for the program intent API views
"""
import datetime
import json
import uuid

import ddt
from django.urls import reverse

from program_intent_engagement.apps.api.v1.views import MostRecentAndCertainIntentsView
from program_intent_engagement.apps.core.models import ProgramIntent
from test_utils import ProgramIntentAPITestCase
from test_utils.factories import UserFactory


@ddt.ddt
class ProgramIntentsViewTests(ProgramIntentAPITestCase):
    """
    Tests Program Intents View
    """

    def setUp(self):
        super().setUp()

        self.url = reverse("api:v1:program_intent-insert")

        self.program_uuid = str(uuid.uuid4())
        self.data = {
            "program_uuid": self.program_uuid,
            "reason": "ALL_COURSES_COMPLETE",
            "certainty": "CERTAIN_YES",
            "effective_timestamp": "2022-07-01 00:00:00",
        }

    def post_api(self, user, data):
        """
        Helper function to make a POST request to the API
        """
        data = json.dumps(data)
        headers = self.build_jwt_headers(user)

        return self.client.post(
            self.url, data, **headers, content_type="application/json"
        )

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
        intent = ProgramIntent.objects.get(
            program_uuid=self.program_uuid,
            reason="ALL_COURSES_COMPLETE",
            certainty="CERTAIN_YES",
            effective_timestamp="2022-07-01 00:00:00",
        )
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
            "program_uuid": self.program_uuid,
            "certainty": "CERTAIN_YES",
            "effective_timestamp": "2022-07-01 00:00:00",
        }
        self.validate_response_code(self.user, data, 400)

    def test_invalid_certainty(self):
        """
        Test that endpoint returns 400 if program intent certainty is invalid
        """
        data = {
            "program_uuid": self.program_uuid,
            "reason": "ALL_COURSES_COMPLETE",
            "certainty": "YES",
            "effective_timestamp": "2022-07-01 00:00:00",
        }
        self.validate_response_code(self.user, data, 400)

    def test_unique_program_intents(self):
        """
        Test that similar program intents with distinct reason fields are both inserted and 200 is returned.
        """
        data_similar = {
            "program_uuid": self.program_uuid,
            "reason": "BUNDLE_PURCHASE",
            "certainty": "CERTAIN_YES",
            "effective_timestamp": "2022-07-01 00:00:00",
        }
        self.validate_response_code(self.user, self.data, 200)
        self.validate_response_code(self.user, data_similar, 200)
        self.assertEqual(len(ProgramIntent.objects.all()), 2)

    def test_distinct_effective_timestamp_program_intents(self):
        """
        Test that similar program intents with distinct effective timestamps are both inserted and 200 is returned.
        """
        data_similar = {
            "program_uuid": self.program_uuid,
            "reason": "ALL_COURSES_COMPLETE",
            "certainty": "CERTAIN_YES",
            "effective_timestamp": "2022-07-02 00:00:00",
        }
        self.validate_response_code(self.user, self.data, 200)
        self.validate_response_code(self.user, data_similar, 200)
        self.assertEqual(len(ProgramIntent.objects.all()), 2)


@ddt.ddt
class ProgramIntentRecentAndCertainViewTests(ProgramIntentAPITestCase):
    """
    Tests MostRecentAndCertainIntentsView
    """

    def setUp(self):
        super().setUp()

        self.program_id1 = str(uuid.uuid4())
        self.program_id2 = str(uuid.uuid4())

        self.p1_intent_maybe = ProgramIntent.objects.create(
            lms_user_id=self.user.lms_user_id,
            program_uuid=self.program_id1,
            reason="a reason",
            certainty="MAYBE",
            effective_timestamp=datetime.datetime(2020, 8, 17),
        )

    def get_api(self, user):
        """
        Helper function to make a get request to the API
        """
        url = reverse("api:v1:intents-list")

        headers = self.build_jwt_headers(user)
        return self.client.get(url, **headers)

    def get_response(self, user):
        """
        Helper function to get API response
        """
        response = self.get_api(user)
        return response

    def test_user_no_intents(self):
        """
        Test that when user has no program intents you get 200 ok response with an empty list
        """
        new_user = UserFactory()

        response = self.get_response(new_user)

        expected_data = []
        expected_status_code = 200

        self.assertEqual(response.status_code, expected_status_code)

        self.assertEqual(response.data, expected_data)

    def test_correct_user_intents(self):
        """
        Test that it only grabs for the input user
        """

        new_user = UserFactory(lms_user_id=2)

        p2_intent_certain_new_user = ProgramIntent.objects.create(
            lms_user_id=new_user.lms_user_id,
            program_uuid=self.program_id2,
            reason="a reason",
            certainty="CERTAIN_NO",
            effective_timestamp=datetime.datetime(2021, 7, 17),
        )

        response = self.get_response(new_user)

        expected_status_code = 200
        expected_lms_user_id = p2_intent_certain_new_user.lms_user_id

        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["lms_user_id"], expected_lms_user_id)

    def test_maybe_intent_taken_if_no_certain(self):
        """
        Test that when user only has maybe program intents it returns the most recent
        """

        p1_intent_maybe2 = ProgramIntent.objects.create(
            lms_user_id=self.user.lms_user_id,
            program_uuid=self.program_id1,
            reason="a reason",
            certainty="CERTAIN_YES",
            effective_timestamp=datetime.datetime(2022, 5, 17),
        )

        response = MostRecentAndCertainIntentsView.grab_best_intents(
            ProgramIntent.objects
        )
        response_list = list(response.values())

        self.assertEqual(len(response.values()), 1)

        actual_timestamp = response_list[0]["effective_timestamp"].strftime("%x")
        expected_timestamp = p1_intent_maybe2.effective_timestamp.strftime("%x")

        self.assertEqual(actual_timestamp, expected_timestamp)

    def test_certain_and_recent_priority(self):
        """
        Test that even when there's a more recent maybe it grabs the most recent certain
        """

        p1_intent_certain = ProgramIntent.objects.create(
            lms_user_id=self.user.lms_user_id,
            program_uuid=self.program_id1,
            reason="a reason",
            certainty="CERTAIN_YES",
            effective_timestamp=datetime.datetime(2020, 5, 17),
        )

        response = MostRecentAndCertainIntentsView.grab_best_intents(
            ProgramIntent.objects
        )

        expected_value = p1_intent_certain.certainty
        actual_value = response[uuid.UUID(self.program_id1)]["certainty"]

        self.assertEqual(len(response.values()), 1)
        self.assertEqual(actual_value, expected_value)

    def test_multiple_intents(self):
        """
        Test that when user has multiple program intents you get the correct responses
        """

        p2_intent_certain = ProgramIntent.objects.create(
            lms_user_id=self.user.lms_user_id,
            program_uuid=self.program_id2,
            reason="a reason",
            certainty="CERTAIN_NO",
            effective_timestamp=datetime.datetime(2021, 7, 17),
        )
        ProgramIntent.objects.create(
            lms_user_id=self.user.lms_user_id,
            program_uuid=self.program_id2,
            reason="a reason",
            certainty="MAYBE",
            effective_timestamp=datetime.datetime(2021, 9, 17),
        )

        response = MostRecentAndCertainIntentsView.grab_best_intents(
            ProgramIntent.objects
        )
        responses_list = list(response.values())

        self.assertEqual(len(response.values()), 2)

        actual_certainties = [
            responses_list[0]["certainty"],
            responses_list[1]["certainty"],
        ]

        self.assertIn(self.p1_intent_maybe.certainty, actual_certainties)
        self.assertIn(p2_intent_certain.certainty, actual_certainties)
