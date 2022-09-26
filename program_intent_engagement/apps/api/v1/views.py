"""
V1 API Views
"""
from itertools import groupby
from operator import itemgetter

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from program_intent_engagement.apps.api.serializers import ProgramIntentSerializer
from program_intent_engagement.apps.core.models import ProgramIntent


class ProgramIntentsView(APIView):
    """
    View to insert program intents.

    Given a valid program intent, this view will insert the program intent. If the given program intent already
    exists, duplicate is not added.

    Path: /api/[version]/program_intents

    Accepts: [POST]

    HTTP POST: Inserts a Program Intent

    Expected POST data: {
        "program_uuid": "949d5e37-e16c-4e95-9104-8c2807caa8ce",
        "reason": "ALL_COURSES_COMPLETE",
        "certainty": "CERTAIN_YES",
        "effective_timestamp": "2022-07-01 00:00:00"
    }

    POST data parameters:
     * program_uuid: The uuid of the program intent.
     * reason: The reason for how intent was measured.
     * certainty: The certainty of the intent for the user.
     * effective_timestamp: When the event occurred that created the intent.
    Returns:
     * 200: The program intent was inserted. If duplicate, no action was taken.
     * 400: The program intent request was invalid or is a duplicate.
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def add_program_intent_lms_user_id(cls, request):
        """
        Add lms_user_id to program intent serializer from request user
        """
        # get lms user id from the request user and add to program intent request
        request.data["lms_user_id"] = request.user.lms_user_id

        return ProgramIntentSerializer(data=request.data)

    def post(self, request):
        """
        Create and insert a program intent. Duplicates not inserted.
        """
        serializer = self.add_program_intent_lms_user_id(request)

        if serializer.is_valid():
            serializer.save()
            response_status = status.HTTP_200_OK
            data = {}
        else:
            response_status = status.HTTP_400_BAD_REQUEST
            data = {"detail": "Invalid data", "errors": serializer.errors}

        return Response(status=response_status, data=data)


class MostRecentAndCertainIntentsView(APIView):
    """
    Retrieve a list of user intents
    This endpoint returns a list of intents specified by the user.
      Grouped by programs and sorted by most recent
      and CERTAIN (if available, otherwise MAYBE) intent
    Path: /api/[version]/program_intents/most_recent_and_certain
    Returns:
     * 200: OK, list of intents
     * 404: User not found
    """

    authentication_classes = (JwtAuthentication,)
    serializer_class = ProgramIntentSerializer

    @classmethod
    def grab_best_intents(cls, user_intents):
        """Given a queryset of intents by program_uuid
          returns a dictionary of best intent per program

        Args:
            user_intents (QuerySet): A queryset of ProgramIntent Objects

        Returns:
            Dict: A dictionary with program_uuid as keys and program_intent as values
        """
        best_intents_dict = {}

        # sorting priority for certainty
        certainty_order = {"CERTAIN_YES": 1, "CERTAIN_NO": 1, "MAYBE": 2}

        sorted_intents_list = list(user_intents.values().order_by("program_uuid"))

        # groupby requires a list sorted by the key (program_uuid)
        for program_uuid, intents in groupby(
            sorted_intents_list, lambda x: x["program_uuid"]
        ):
            intents = list(intents)

            # sort by effective_timestamp descending, then certainty ascending
            intents.sort(
                key=itemgetter("effective_timestamp"),
                reverse=True,
            )

            intents.sort(
                key=lambda x: (
                    certainty_order[(x["certainty"])],
                ),
            )

            # grab the top intent
            best_intents_dict[program_uuid] = intents[0]

        return best_intents_dict

    def get(self, request):
        """
        This view should return the best intents per program
        for the currently authenticated user.

        Best intent is defined as the most recent CERTAIN intent
        or the most recent MAYBE intent if a CERTAIN intent does not exist.
        """

        # test that user is populated is not enough, the anonymous user exists but has no lms ID
        if not self.request.user or not hasattr(self.request.user, "lms_user_id"):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        lms_user_id = self.request.user.lms_user_id

        user_intents = ProgramIntent.objects.filter(lms_user_id=lms_user_id)

        best_intents = self.grab_best_intents(user_intents)

        if best_intents:
            response_status = status.HTTP_200_OK
            data = list(best_intents.values())
        else:
            response_status = status.HTTP_200_OK
            data = []

        return Response(status=response_status, data=data)
