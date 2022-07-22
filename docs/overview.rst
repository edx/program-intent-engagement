PIE Service Overview
--------------------
The program intent and engagement (PIE) service is a data store used to capture
various interactions a user could have with a program and its courses.

Users of the service can query it for a user's intents, or create new intents
via HTTP request or management command.

Program Intent Model
~~~~~~~~~~~~~~~~~~~~
The program intent model is meant to represent when a learner marked an interest in a program, why we believe
their action represents an intent, and how certain we are of their intent to participate in a program.

The types of intent reasons and their corresponding certainty are described in the following table:

+----------------------+--------------------------------------------+-------------+
| Reason               | Description                                | Certainty   |
+======================+============================================+=============+
| BUNDLE_PURCHASE      | User purchased program as a bundle         | CERTAIN_YES |
+----------------------+--------------------------------------------+-------------+
| ENROLLED_ALL_COURSES | User has enrolled in all program courses   | MAYBE       |
+----------------------+--------------------------------------------+-------------+
| EARNED_PROGRAM_CERT  | User has earned a program certificate      | CERTAIN_YES |
+----------------------+--------------------------------------------+-------------+

While these are the current intent reasons, users have the ability to add more if needed. It should also
be noted that users also have the ability to add an intent with a `CERTAIN_NO` certainty, although none of
our current intent definitions correspond with that certainty.

Accessing Learner Intents
~~~~~~~~~~~~~~~~~~~~~~~~~
Learner intents can be queried via HTTP GET request. The request user will be used to filter
intents, so only intents associated with that user will be returned.

Currently the implementation will only return the most recent and most certain intent
per program for each user. This means the endpoint will return

- the most recent `CERTAIN_YES` or `CERTAIN_NO` for a program
- if there is no certain intent, return the most recent `MAYBE` for a program

Inserting Learner Intents
~~~~~~~~~~~~~~~~~~~~~~~~~
There are two methods to create new learner intents:

- HTTP POST request
- Insert management command

A learner intent can be created via HTTP POST request, and intents can only be created for the requesting user. The API expects the request data to contain::

    program_uuid: program UUID to be associated with the attempt
    reason: reason we believe the learner intends to participate in the program
    certainty: how certain we are that the reason corresponds to a learner's intentions
    effective_timestamp: datetime for when the intent was expressed (e.g. datetime of when a learner purchased a program as a bundle)

If a user attempts to create a duplicate intent via HTTP request, a 400 response will be returned.

Learner intents can also be bulk created via `bulk_insert_intents` management command. The command expects a CSV with a
header row as input, with each row defined in the CSV representing an intent that should be created. The expected columns for
the data are::

    program_uuid
    user_id (LMS user ID, as opposed to PIE service user ID)
    intent_reason
    intent_certainty
    effective_time

If a duplicate intent is defined in the CSV file, the management command will not attempt to create a new intent for that duplicate data.
