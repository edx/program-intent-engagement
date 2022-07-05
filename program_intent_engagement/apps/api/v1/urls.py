""" API v1 URLs. """
from django.urls import re_path

from . import views

app_name = "v1"

urlpatterns = [
    re_path(
        r"^program_intents/?$",
        views.ProgramIntentsView.as_view(),
        name="program_intent-insert",
    ),
    re_path(
        r"^intents/most-recent-and-certain?$",
        views.MostRecentAndCertainIntentsView.as_view(),
        name="intents-list",
    ),
]
