Installation
============

Installation is fairly straight forward. It boils down to 3 steps.

1. Download the source.
2. Add it to ``INSTALLED_APPS``
3. Use it.

Download the source
-------------------

To get the source, you can find it on `github`_. I would suggest
installing it with ``pip``. That looks more or less like..

::

  pip install -e git+http://github.com/justinlilly/django-gencal.git#egg=django_gencal

Add it to ``INSTALLED_APPS``
----------------------------

Fairly straight-forward as well.

::

  INSTALLED_APPS = (
    ...
    'gencal',
    ...
  )

Use it
------

As for use, check out the rest of the :doc:`templatetag` documentation.

.. _github: http://github.com/justinlilly/django-gencal/
