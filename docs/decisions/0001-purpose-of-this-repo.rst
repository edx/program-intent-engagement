1. Purpose of this Repo
=======================

Status
------

Accepted

Context
-------

Currently we have very little reliable tracking of learners' engagement with programs unless they directly purchase a program bundle or Masters. The program intent engagement service will track that engagement so that we can use it in reporting and personalization.


Decision
--------

Since program intent is a new concept and may be sourced from multiple existing services it makes sense to have it as a separate entity in the system. Some users of open edX may wish to adopt the PIE service, but it is purely additive and will not be necessary to run open edX.

Consequences
------------

Once the PIE service is ready it will be used to drive other projects such as personalization. MFEs and others will also write program intents into the service.

Rejected Alternatives
---------------------

The major competitor for program intent is to develop a complete stateful model of program enrollment tangled with the learners and courses. We want to push as much as possible out of edx-platform.
