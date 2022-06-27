""" Core models. """

import django.utils.timezone
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
    lms_user_id = models.IntegerField(null=True, db_index=True)

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
    """
    REASON = (
        ('CC', 'All Courses Complete'),
        ('BP', 'Bundle Purchase'),
        ('CE', 'All Courses Enrolled'),
    )
    CERTAINTY = (
        ('Y', 'Certainly Yes'),
        ('N', 'Certainly No'),
        ('M', 'Maybe'),
    )

    #
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)

    program_uuid = models.UUIDField()

    # The specific reason for how intent was measured.
    reason = models.CharField(max_length=255, db_index=True)

    # Another approach to reason using enum choice field
    reason = models.CharField(
        max_length=2,
        choices=REASON)

    # The certainty of the program intent for the user.
    certainty = models.CharField(
        max_length=1,
        choices=CERTAINTY)

    # When did the event occurred that made this intent.
    effective_date = models.DateTimeField(default=django.utils.timezone.now)

    # is there an existing db we should refer to?
    class Meta:
        """ Meta class for this Django model """
        db_table = 'programintent_programintent'
        verbose_name = 'program intent'
        unique_together = ('user', 'program_uuid', 'reason', 'certainty', 'effective_date',)
