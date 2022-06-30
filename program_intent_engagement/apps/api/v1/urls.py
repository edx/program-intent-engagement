""" API v1 URLs. """
from django.urls import re_path

from program_intent_engagement.apps.api.v1.views import ProgramIntentsView

app_name = 'v1'

urlpatterns = [
    re_path(r'^program_intents/?$',
            ProgramIntentsView.as_view(),
            name='program_intent-insert'),
]
