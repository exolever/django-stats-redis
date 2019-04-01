=============================
django-stats-redis
=============================

.. image:: https://badge.fury.io/py/django-stats-redis.svg
    :target: https://badge.fury.io/py/django-stats-redis

.. image:: https://requires.io/github/exolever/django-stats-redis/requirements.svg?branch=master
     :target: https://requires.io/github/exolever/django-stats-redis/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/exolever/django-stats-redis.svg?branch=master
    :target: https://travis-ci.org/exolever/django-stats-redis

.. image:: https://codecov.io/gh/exolever/django-stats-redis/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/exolever/django-stats-redis

.. image:: https://sonarcloud.io/api/project_badges/measure?project=exolever_django-stats-redis&metric=alert_status
   :target: https://sonarcloud.io/dashboard?id=exolever_django-stats-redis
   
.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/exolever/django-stats-redis/issues
   
.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT


Manage stats within Redis for Django models


Quickstart
----------

Install stats::

    pip install django-stats-redis

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'stats',
        ...
    )

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
