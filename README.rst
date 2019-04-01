=============================
django-stats-mixin
=============================

.. image:: https://badge.fury.io/py/django-stats.svg
    :target: https://badge.fury.io/py/django-stats-mixin

.. image:: https://travis-ci.org/marfyl/django-stats.svg?branch=master
    :target: https://travis-ci.org/marfyl/django-stats

.. image:: https://codecov.io/gh/marfyl/django-stats/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/marfyl/django-stats


Quickstart
----------

Install stats::

    pip install django-stats-mixin

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
