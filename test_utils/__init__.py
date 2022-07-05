"""
Test utilities.
"""

from rest_framework.test import APIClient, APITestCase

from test_utils.factories import UserFactory
from test_utils.mixins import JwtMixin

TEST_USERNAME = 'api_worker'
TEST_EMAIL = 'test@email.com'
TEST_PASSWORD = 'QWERTY'
TEST_LMS_USER_ID = 1


class ProgramIntentAPITestCase(JwtMixin, APITestCase):
    """
    Base class for API Tests
    """

    def setUp(self):
        """
        Perform operations common to all tests.
        """
        super().setUp()
        self.create_user(username=TEST_USERNAME, email=TEST_EMAIL, password=TEST_PASSWORD, lms_user_id=TEST_LMS_USER_ID,
                         is_staff=False)
        self.client = APIClient()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def tearDown(self):
        """
        Perform common tear down operations to all tests.
        """
        # Remove client authentication credentials
        self.client.logout()
        super().tearDown()

    def create_user(self, username=TEST_USERNAME, password=TEST_PASSWORD, is_staff=False, lms_user_id=TEST_LMS_USER_ID,
                    **kwargs):
        """
        Create a test user and set its password.
        """
        self.user = UserFactory(username=username, is_active=True, is_staff=is_staff, lms_user_id=lms_user_id, **kwargs)
        self.user.set_password(password)
        self.user.save()

    def build_jwt_headers(self, user):
        """
        Set jwt token in cookies.
        """
        jwt_payload = self.default_payload(user)
        jwt_token = self.generate_token(jwt_payload)
        headers = {"HTTP_AUTHORIZATION": "JWT " + jwt_token}
        return headers
