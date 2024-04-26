# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/edx/program-intent-engagement/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                                                    |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------------------------------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| program\_intent\_engagement/\_\_init\_\_.py                                                             |        1 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/\_\_init\_\_.py                                                        |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/\_\_init\_\_.py                                                    |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/models.py                                                          |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/serializers.py                                                     |        6 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/tests/\_\_init\_\_.py                                              |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/urls.py                                                            |        4 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/v1/\_\_init\_\_.py                                                 |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/v1/tests/\_\_init\_\_.py                                           |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/v1/tests/test\_views.py                                            |      122 |        0 |        4 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/v1/urls.py                                                         |        4 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/api/v1/views.py                                                        |       51 |        0 |       15 |        2 |     97% |51->50, 93->92 |
| program\_intent\_engagement/apps/core/\_\_init\_\_.py                                                   |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/constants.py                                                      |        3 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/context\_processors.py                                            |        3 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/management/\_\_init\_\_.py                                        |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/management/commands/\_\_init\_\_.py                               |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/management/commands/bulk\_insert\_intents.py                      |       38 |        0 |       10 |        2 |     96% |53->exit, 92->53 |
| program\_intent\_engagement/apps/core/management/tests/\_\_init\_\_.py                                  |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/management/tests/test\_bulk\_insert\_intents.py                   |       16 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/migrations/0001\_initial.py                                       |        8 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/migrations/0002\_user\_lms\_user\_id.py                           |        4 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/migrations/0003\_programintent.py                                 |        8 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/migrations/0004\_programintent\_lms\_user\_id.py                  |        4 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/migrations/0005\_remove\_programintent\_lms\_user\_id\_default.py |        4 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/migrations/0006\_alter\_user\_lms\_user\_id.py                    |        4 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/migrations/\_\_init\_\_.py                                        |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/models.py                                                         |       30 |        0 |        2 |        1 |     97% |    22->21 |
| program\_intent\_engagement/apps/core/tests/\_\_init\_\_.py                                             |        0 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/tests/test\_context\_processors.py                                |        8 |        0 |        2 |        1 |     90% |    14->13 |
| program\_intent\_engagement/apps/core/tests/test\_models.py                                             |       30 |        0 |        0 |        0 |    100% |           |
| program\_intent\_engagement/apps/core/tests/test\_views.py                                              |       37 |        0 |        6 |        3 |     93% |25->exit, 49->48, 55->54 |
| program\_intent\_engagement/apps/core/views.py                                                          |       38 |        0 |        6 |        1 |     98% |    20->19 |
| program\_intent\_engagement/docker\_gunicorn\_configuration.py                                          |       27 |       27 |       10 |        0 |      0% |      4-57 |
| program\_intent\_engagement/urls.py                                                                     |       10 |        0 |        0 |        0 |    100% |           |
|                                                                                               **TOTAL** |  **460** |   **27** |   **55** |   **10** | **91%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/edx/program-intent-engagement/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/edx/program-intent-engagement/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/edx/program-intent-engagement/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/edx/program-intent-engagement/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fedx%2Fprogram-intent-engagement%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/edx/program-intent-engagement/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.