"""
V1 API Views
"""
import logging

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from program_intent_engagement.apps.api.serializers import ProgramIntentSerializer

log = logging.getLogger(__name__)


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
