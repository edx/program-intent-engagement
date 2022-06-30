""" Core models. """

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class User(AbstractUser):
    """
    Custom user model for use with python-social-auth via edx-auth-backends.

    .. pii: Stores full name, username, and email address for a user.
    .. pii_types: name, username, email_address
    .. pii_retirement: local_api

    """
    full_name = models.CharField(_('Full Name'), max_length=255, blank=True, null=True)
    lms_user_id = models.IntegerField(null=True, db_index=True, unique=True)

    @property
    def access_token(self):
        """
        Returns an OAuth2 access token for this user, if one exists; otherwise None.
        Assumes user has authenticated at least once with the OAuth2 provider (LMS).
        """
        try:
            return self.social_auth.first().extra_data['access_token']  # pylint: disable=no-member
        except Exception:  # pylint: disable=broad-except
            return None

    class Meta:
        get_latest_by = 'date_joined'

    def get_full_name(self):
        return self.full_name or super().get_full_name()

    def __str__(self):
        return str(self.get_full_name())


class ProgramIntent(TimeStampedModel):
    """
    Information about the Program intent

    .. no_pii:
    """

    CERTAINTY = (
        ('CERTAIN_YES', 'CERTAIN_YES'),
        ('CERTAIN_NO', 'CERTAIN_NO'),
        ('MAYBE', 'MAYBE'),
    )

    lms_user_id = models.IntegerField(db_index=True)

    program_uuid = models.UUIDField()

    # The specific reason for how intent was measured.
    reason = models.CharField(
        max_length=255,
        null=False)

    # The certainty of the program intent for the user.
    certainty = models.CharField(
        max_length=255,
        choices=CERTAINTY,
        null=False)

    # When did the event occurred that made this intent.
    effective_timestamp = models.DateTimeField()

    class Meta:
        """ Meta class for this Django model """
        db_table = 'programintent_programintent'
        verbose_name = 'program intent'
        unique_together = ('lms_user_id', 'program_uuid', 'reason', 'certainty', 'effective_timestamp',)
