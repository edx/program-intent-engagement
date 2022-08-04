""" API v1 URLs. """
from django.urls import re_path

from program_intent_engagement.apps.api.v1.views import MostRecentAndCertainIntentsView, ProgramIntentsView

app_name = "v1"

urlpatterns = [
    re_path(
        r"^program_intents/?$",
        ProgramIntentsView.as_view(),
        name="program_intent-insert",
    ),
    re_path(
        r"^program_intents/most_recent_and_certain?$",
        MostRecentAndCertainIntentsView.as_view(),
        name="intents-list",
    ),
]
