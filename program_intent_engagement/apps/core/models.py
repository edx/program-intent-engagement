""" Core models. """

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
# TODO: ask alie how to import (using requirements)


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
    Information about the Program Intent.

    .. no_pii:
    """

    # TODO: how should this be displayed?
    class IntentCertainty(models.TextChoices):
        CERTAIN_YES = 'Y', _('Certain Yes')
        CERTAIN_NO = 'N', _('Certain No')
        MAYBE = 'M', _('Certain Maybe')

    # TODO: read about db index and on delete
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)

    program = models.UUIDField()

    # The specific reason for how intent was measured.
    reason = models.CharField(max_length=255, db_index=True)

    # TODO: would a default be useful?
    # The certainty of the program intent for the user.
    certainty = models.CharField(max_length=1, choices=IntentCertainty.choices)

    # When the event that made this intent occurred.
    effective_time = models.DateTimeField(null=True)

    # TODO: is meta naming correct?
    class Meta:
        """ Meta class for this Django model """
        db_table = 'pie_program_intent'
        verbose_name = 'program_intent'
        # TODO: is this the right unique together?
        # TODO: why is there an extra comma?
        unique_together = (('user', 'program'),)


